import http.server
import json
import logging
import requests
import base64
import os
from datetime import datetime
import time
import threading
class camStatus:
    def __init__(self):
        self.needToOpen = False
        self.needToClose = False
        self.serialDataToSend = {"0":[], "1":[]} #Data Queue to send to LED by serialdata
        self.heartbeatToSend = {"0":[], "1":[]} #Data Queue to send to LED by heartbeat
        self.carQueue = [] #Car Info Queue waiting for gio
        self.carGio0 = 1 #Camera  Gio0 status
        self.carGio1 = 1 #Camera  Gio1 status
        
class MyHandler(http.server.BaseHTTPRequestHandler):
    AlarmInfoPlate = "AlarmInfoPlate"
    AlarmGioIn = "AlarmGioIn"
    heartbeat = "heartbeat"
    SerialData = "SerialData"
    Response_AlarmInfoPlate = "Response_AlarmInfoPlate"
    Response_SerialData = "Response_SerialData"
    Response_Heartbeat = "Response_Heartbeat"
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
            response = self.handle_request(data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Invalid JSON"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    def handle_request(self, data):
        if "AlarmInfoPlate" in data:
            response = self.check_car(data)
        elif "heartbeat" in data:
            response = self.getHeartbeatResponse(self.client_address[0])
        elif "AlarmGioIn" in data:
            response = self.handleGioData(data)
        elif "SerialData" in data:
            response = self.getSerialDataResponse(data)
        
        return response
    
    def log_message(self, format, *args):
        pass
    #waiting Gio0 be triggered and add car data to queue
    def waitForGio0Triggered(self, in_out, data, ip, car_number):
        for i in range(0, 200):
            time.sleep(0.05)
            if in_out == "0":
                if cam_status[ip].carGio0 == 0:
                    cam_status[ip].carQueue.append(data)
                    cam_status[ip].needToOpen = True
                    threading.Thread(target=self.waitForGio1Triggered, args=(in_out, ip)).start()
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                    setWelcomeSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                    break
            else:
                if cam_status[ip].carGio0 == 0:
                    cam_status[ip].needToOpen = True
                    cam_status[ip].carQueue.append(data)
                    threading.Thread(target=self.waitForGio1Triggered, args=(in_out, ip)).start()
                    #set thank u to XXXXXXX
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                    setThankUSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                    break
    def waitForGio1Triggered(self, in_out, ip):
        needPop = True
        for i in range(0, 400):
            time.sleep(0.05)
            if in_out == "0":
                if cam_status[ip].carGio1 == 0:
                    updateCarInside(ip)
                    #set LED0 and LED1 to slot left
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["1"])
                    setCarSlotsBig(ip)
                    setCarSlotsSmall(ip)
                    needPop = False
                    refreshCarSlot(ip)
                    break
            else:
                if cam_status[ip].carGio1 == 0:
                    updateHistory(ip)
                    #set LED0 to pay before leave and LED1 to slot left
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["1"])
                    setCarSlotsBig(ip)
                    setOutNormalScreen(ip)
                    needPop = False
                    refreshCarSlot(ip)
                    break
        # GIO1 not triggered, dispose data
        if needPop:
            if in_out == "0":
                cam_status[ip].carQueue.pop(0)
            else:
                cam_status[ip].carQueue.pop(0)
    def getHeartbeatResponse(self, ip):
        res = {
            "Response_Heartbeat": {
                "info": "no",
                "serialData": [],
                "shutoff": "no",
                "snapnow": "no"
                }
        }
        #check if need to open the gate from SQL database
        cam = getIpCam(ip)
        if cam is None:
            return res
        cam_in_out = "0"
        if "in_out" in cam:
            cam_in_out = cam["in_out"]
        if "open" in cam:
            open = cam["open"]
            #update cam with gate close
            updateCamNotToOpen(ip)
        if "close" in cam:
            close = cam["close"]
            if close == "1":
                updateCamNotToClose(ip)
        cam_status[ip].needToOpen = cam_status[ip].needToOpen or open == "1"
        if cam_status[ip].needToOpen:
            cam_status[ip].needToOpen = False
            res["Response_Heartbeat"]["info"] = "ok"
        cam_status[ip].needToClose = cam_status[ip].needToClose or close == "1"
        if cam_status[ip].needToClose:
            cam_status[ip].needToClose = False
            res["Response_Heartbeat"]["shutoff"] = "ok"
        #check if heartbeat has serial data
        if ip in cam_status:
            if len(cam_status[ip].heartbeatToSend["0"]) > 0:
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 0,
                    "data": cam_status[ip].heartbeatToSend["0"].pop(0),
                    "dataLen": 38
                })
            if len(cam_status[ip].heartbeatToSend["1"]) > 0:
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 1,
                    "data": cam_status[ip].heartbeatToSend["1"].pop(0),
                    "dataLen": 38
                })
        return res
    def handleGioData(self, data):
        ip = data["AlarmGioIn"]["ipaddr"]
        serial_num = data["AlarmGioIn"]["result"]["TriggerResult"]["source"]
        serial_value = data["AlarmGioIn"]["result"]["TriggerResult"]["value"]
        
        cam = getIpCam(ip)
        if cam is None:
            return ""
        cam_in_out = "0"
        if "in_out" in cam:
            cam_in_out = cam["in_out"]
        if serial_num == 0:
            cam_status[ip].carGio0 = serial_value
        else:
            original = cam_status[ip].carGio1
            cam_status[ip].carGio1 = serial_value
            if original==0 and serial_value==1:
                cam_status[ip].needToClose = True
        # if cam_in_out == "0":
        #     if serial_num == 0:
        #         cam_status[ip].carGio0 = serial_value
        #     else:
        #         cam_status[ip].carGio0 = serial_value
        #         # if cam_status.carInGio1 == 1 and cam_status.carInGio0 ==1:
        #         #     cleanLEDSerialData(cam_status.heartbeatToSend[ip]["0"])
        #         #     setCarSlotsBig(ip, cam_status)
        #         #     setCarSlotsSmall(ip, cam_status)
        # else:
        #     if serial_num == 0:
        #         cam_status[ip].carGio0 = serial_value
        #     else:
        #         cam_status[ip].carGio0 = serial_value
        #         # if cam_status.carOutGio1 == 1 and cam_status.carOutGio0 ==1:
        #         #     cleanLEDSerialData(cam_status.heartbeatToSend[ip]["0"])
        #         #     setCarSlotsBig(ip, cam_status)
        #         #     setCarSlotsSmall(ip, cam_status)
        return ""
    def getSerialDataResponse(self, data):
        res = {
            "Response_SerialData": {
                "info": "no",
                "serialData":[
                ]
            }
        }
        ip = data["SerialData"]["ipaddr"]
        if ip in cam_status:
            if len(cam_status[ip].serialDataToSend["0"]) > 0:
                res["Response_SerialData"]["serialData"].append({
                    "serialChannel": 0,
                    "data": cam_status[ip].serialDataToSend["0"].pop(0),
                    "dataLen": 38
                })
            if len(cam_status[ip].serialDataToSend["1"]) > 0:
                res["Response_SerialData"]["serialData"].append({
                    "serialChannel": 1,
                    "data": cam_status[ip].serialDataToSend["1"].pop(0),
                    "dataLen": 38
                })
        return res
    def check_car(self, data):
        # response for picture
        response = {
                "Response_AlarmInfoPlate": {
                    "info": "no",
                    "content": "retransfer_stop",
                    "is_pay": "true",
                    "serialData": [{"serialChannel": 0,	"data": "",	"dataLen": 0}, {"serialChannel": 1,	"data": "",	"dataLen": 0}]
                    }
                }
        #car detailed data
        reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
        ip = data["AlarmInfoPlate"]["ipaddr"]
        car_number = reselt["license"]
        # get ip cam data
        cam = getIpCam(ip)
        if cam is None:
            return response
        cam_in_out = "0"
        if "in_out" in cam:
            cam_in_out = cam["in_out"]
        read_gio = "0"
        if "read_gio" in cam:
            read_gio = cam["read_gio"]
        if cam_in_out == "0":
            if checkCanIn(data):
                if read_gio == '1':
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    # cam_status[ip].carQueue.append(data)
                    # updateCarInside(ip)
                    response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    response["Response_AlarmInfoPlate"]["serialData"][1]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][1]["dataLen"] = 38
                    setCarSlotsBig(ip)
                    setWelcomeSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                    cleanLEDSerialData(cam_status[ip].serialDataToSend["0"])
                    cleanLEDSerialData(cam_status[ip].serialDataToSend["1"])
                    setCarSlotsBig(ip)
                    setCarSlotsSmall(ip)
                    refreshCarSlot(ip)
                else:
                    if cam_status[ip].carGio0 != 0:
                        #gio0 in is not triggered
                        threading.Thread(target=self.waitForGio0Triggered, args=(cam_in_out, data, ip, car_number)).start()
                        return response
                    cam_status[ip].carQueue.append(data)
                    threading.Thread(target=self.waitForGio1Triggered, args=(cam_in_out, ip)).start()
                    # add serial0 data to WELCOME XXXXXXX
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    setWelcomeSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                response["Response_AlarmInfoPlate"]["info"] = "ok"
            else:
                cam_status[ip].heartbeatToSend["0"].clear()
                cam_status[ip].heartbeatToSend["1"].clear()
                cam_status[ip].serialDataToSend["0"].clear()
                cam_status[ip].serialDataToSend["1"].clear()
                response["Response_AlarmInfoPlate"]["info"] = "no"
                #add serial0 data to full and wait
                response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                setCarSlotsSmall(ip)
        else:
            if checkCanOut(data):
                if read_gio == '1':
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cam_status[ip].carQueue.append(data)
                    updateHistory(ip)
                    response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    response["Response_AlarmInfoPlate"]["serialData"][1]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][1]["dataLen"] = 38
                    setCarSlotsBig(ip)
                    setThankUSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                    cleanLEDSerialData(cam_status[ip].heartbeatToSend["1"])
                    setCarSlotsBig(ip)
                    setOutNormalScreen(ip)
                    refreshCarSlot(ip)
                else:
                    if cam_status[ip].carGio0 != 0:
                        #gio0 out is not triggered
                        threading.Thread(target=self.waitForGio0Triggered, args=(cam_in_out, data, ip, car_number)).start()
                        return response
                    cam_status[ip].carQueue.append(data)
                    threading.Thread(target=self.waitForGio1Triggered, args=(cam_in_out, ip)).start()
                    #set thank u to XXXXXXX
                    response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    cam_status[ip].heartbeatToSend["0"].clear()
                    cam_status[ip].heartbeatToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    setThankUSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                response["Response_AlarmInfoPlate"]["info"] = "ok"
            else:
                cam_status[ip].heartbeatToSend["0"].clear()
                cam_status[ip].heartbeatToSend["1"].clear()
                cam_status[ip].serialDataToSend["0"].clear()
                cam_status[ip].serialDataToSend["1"].clear()
                response["Response_AlarmInfoPlate"]["info"] = "no"
                #add serial0 data to need to pay
                response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                setNeedToPay(ip)
                setCarNumberSerialData(ip, car_number)
        return response
#update database after car go in
def updateCarInside(ip):
    data = cam_status[ip].carQueue.pop(0)
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    size = "0"
    color = reselt["carColor"]
    image_string = reselt["imageFile"]
    car_number = reselt["license"]
    file_name = "/storage/sdcard/Cars/" + car_number + ".png"
    #add new car and open gate
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(image_string)))
    addCarInside(car_number, "A", file_name, size, color)
#update database after car go out
def updateHistory(ip):
    data = cam_status[ip].carQueue.pop(0)
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    car_number = reselt["license"]
    image_string = reselt["imageFile"]
    file_name = "/storage/sdcard/Cars/" + car_number + ".png"
    backup_file_name = "/storage/sdcard/Cars_backup/" + nowTime.strftime("%Y_%m_%d_%H_%M_%S") + "_" + car_number + ".png"
    carInside = getCarInside(car_number)
    #close gate and show no available car slot
    addHistory(carInside, nowTime.strftime("%Y-%m-%d %H:%M:%S"), backup_file_name)
    deleteCarInside(car_number)
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(backup_file_name, "wb") as fh:
        fh.write(base64.decodebytes(str.encode(image_string)))
#check the car can enter(check slots and cars_inside)
def checkCanIn(data):
    ret = False
    #car detailed data
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    car_number = reselt["license"]
    carInside = getCarInside(car_number)
    available = slotSearch()
    if available > 0 and carInside is None:
        ret = True
    return ret
#check the car can exit(check paytime)
def checkCanOut(data):
    ret = False
    #car detailed data
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    car_number = reselt["license"]
    carInside = getCarInside(car_number)
    if carInside is not None and carInside["time_pay"] is not None and carInside["time_pay"] != "":
        time_pay = carInside["time_pay"]
        nowTime = datetime.now()
        payTime = datetime.strptime(time_pay, "%Y-%m-%d %H:%M:%S")
        diffTime = nowTime-payTime
        seconds = diffTime.seconds
        if seconds <= 900:
            ret = True
    return ret
#check available slots
def slotSearch():
    slot = 0
    #get total cat slots
    myobj = {'func': 'slot_search'}
    x = requests.get(url, params = myobj)
    try:
        data = json.loads(x.text)
        if len(data) > 0:
            data = list(data)
            slot_data = data[0]
            slot = slot + int(slot_data['car_slot'])
            slot = slot + int(slot_data['pregnant_slot'])
            slot = slot + int(slot_data['disabled_slot'])
            slot = slot + int(slot_data['charging_slot'])
            slot = slot + int(slot_data['reserved_slot'])
        else:
            return 0
    except json.JSONDecodeError:
        return 0
    #get number of cars inside
    myobj = {'func': 'cars_inside_count'}
    x = requests.get(url, params = myobj)
    try:
        data = json.loads(x.text)
        if len(data) > 0:
            data = list(data)
            cars_inside = data[0]
            slot = slot - int(cars_inside['COUNT(*)'])
        else:
            return 0
    except json.JSONDecodeError:
        return 0
    return slot
#check if car with car_number is already in database
def isCarInside(car_number):
    data = getCarInside(car_number)

    if data is not None:
        return True
    else:
        return False
#get car with car_number in cars_inside
def getCarInside(car_number):
    myobj = {'func': 'cars_inside_with_car_number'}
    myobj["car_number"] = car_number
    x = requests.get(url, params = myobj)
    data = json.loads(x.text)

    if len(data) > 0:
        data = list(data)
        slot_data = data[0]
        return slot_data
    else:
        return None
#add car to cars_inside after entering
def addCarInside(car_number, gate, picture_url,type,color):
    now = datetime.now()
    time_in = now.strftime("%Y-%m-%d %H:%M:%S")
    myobj = {"Response_AlarmInfoPlate":{}}
    myobj["car_number"] = car_number
    myobj["time_in"] = time_in
    myobj["gate"] = gate
    myobj["picture_url"] = picture_url
    myobj["type"] = type
    myobj["color"] = color
    x = requests.post(url + "?func=cars_inside_add", data = myobj)
#delete car in cars_inside after exiting
def deleteCarInside(car_number):
    myobj = {'func': 'cars_inside_delete'}
    myobj["car_number"] = car_number
    x = requests.get(url, params = myobj)
#add car to history after exiting
def addHistory(car_data, time_out, path):
    myobj = {'func': 'history_add'}
    myobj["car_number"] = car_data["car_number"]
    myobj["time_in"] = car_data["time_in"]
    myobj["time_out"] = time_out
    myobj["time_pay"] = car_data["time_pay"]
    myobj["cost"] = car_data["cost"]
    myobj["bill_number"] = car_data["bill_number"]
    myobj["payment"] = car_data["payment"]
    myobj["artificial"] = car_data["artificial"]
    myobj["type"] = car_data["type"]
    myobj["color"] = car_data["color"]
    myobj["path"] = path
    x = requests.get(url, params = myobj)
#get cam with certain ip in database
def getIpCam(ip):
    myobj = {'func': 'cam_single_search'}
    myobj["ip"] = ip
    x = requests.get(url, params = myobj)
    data = json.loads(x.text)

    if len(data) > 0:
        data = list(data)
        cam = data[0]
        return cam
    else:
        return None
#get all the cams in database
def getIpCams():
    myobj = {'func': 'cam_search'}
    x = requests.get(url, params = myobj)
    data = json.loads(x.text)

    if len(data) > 0:
        data = list(data)
        return data
    else:
        return None
#set ip cam open=0 after open on backend app
def updateCamNotToOpen(ip):
    #update cam open status on SQL
    myobj = {'func': 'cam_update_open'}
    myobj["ip"] = ip
    myobj["open"] = 0
    x = requests.get(url, params = myobj)
def updateCamNotToClose(ip):
    #update cam close status on SQL
    myobj = {'func': 'cam_update_close'}
    myobj["ip"] = ip
    myobj["close"] = 0
    x = requests.get(url, params = myobj)
#init cam dictionay if it's not been initialized
def setCams(ip):
    cam_status[ip] = camStatus()
#in LED 0: welcome
def setWelcomeSerialData(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
    
#in LED 0: $car_number
def setCarNumberSerialData(ip, car_number):
    for i in range(len(car_number)):
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x10 ,0x00 ,0x08 ,0x00 ,0x10 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x01 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        serial_data[12] = i*8
        if car_number[i].isdigit():
            serial_data[32] = string_to_int_small(car_number[i])
        else:
            serial_data[32] = char_to_int(car_number[i])
        cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
# Thank u
def setThankUSerialData(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x37 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
#in/out LED 1 : P xxx
def setCarSlotsBig(ip):
    available = slotSearch()
    P_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x14 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x32 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    cam_status[ip].serialDataToSend["1"].append(getBase64String(P_data))
    if available > 0:
        format_number = '{:03d}'.format(available)
        for i in range(len(format_number)):
            serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
            serial_data[12] = 20+i*14
            serial_data[32] = string_to_int_Big(format_number[i])
            cam_status[ip].serialDataToSend["1"].append(getBase64String(serial_data))
    else:
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x14 ,0x00 ,0x00 ,0x00 ,0x2A ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x33 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        cam_status[ip].serialDataToSend["1"].append(getBase64String(serial_data))
def setCarSlotsBigWithHearbeat(ip):
    available = slotSearch()
    P_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x14 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x32 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    cam_status[ip].heartbeatToSend["1"].append(getBase64String(P_data))
    if available > 0:
        format_number = '{:03d}'.format(available)
        for i in range(len(format_number)):
            serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
            serial_data[12] = 20+i*14
            serial_data[32] = string_to_int_Big(format_number[i])
            cam_status[ip].heartbeatToSend["1"].append(getBase64String(serial_data))
    else:
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x14 ,0x00 ,0x00 ,0x00 ,0x2A ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x33 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        cam_status[ip].heartbeatToSend["1"].append(getBase64String(serial_data))
#in LED 0: how much slots left. if 0, show full, else available slots xxx
def setCarSlotsSmall(ip):
    number = slotSearch()
    if number > 0:
        P_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x35 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        cam_status[ip].serialDataToSend["0"].append(getBase64String(P_data))
        format_number = '{:03d}'.format(number)
        for i in range(len(format_number)):
            serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x10 ,0x00 ,0x08 ,0x00 ,0x10 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
            serial_data[12] = 20+i*8
            serial_data[32] = string_to_int_small(format_number[i])
            cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
    else:
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3D ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
def setCarSlotsSmallWithHeartbeat(ip):
    number = slotSearch()
    if number > 0:
        P_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x35 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        cam_status[ip].heartbeatToSend["0"].append(getBase64String(P_data))
        format_number = '{:03d}'.format(number)
        for i in range(len(format_number)):
            serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x10 ,0x00 ,0x08 ,0x00 ,0x10 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
            serial_data[12] = 20+i*8
            serial_data[32] = string_to_int_small(format_number[i])
            cam_status[ip].heartbeatToSend["0"].append(getBase64String(serial_data))
    else:
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3D ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        cam_status[ip].heartbeatToSend["0"].append(getBase64String(serial_data))
#out LED 0 : not pay yet $car_number
def setNeedToPay(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x38 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
#out LED 0 : pay before leace
def setOutNormalScreen(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3E ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
def  setOutNormalScreenWithHearbeat(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3E ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    cam_status[ip].heartbeatToSend["0"].append(getBase64String(serial_data))
#clear LED
def cleanLEDSerialData(array):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3C ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    array.append(getBase64String(serial_data))
def getCleanLEDSerialData():
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3C ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    return getBase64String(serial_data)
def getBase64String(bytes):
    encoded_string = base64.b64encode(bytes).decode('utf-8')
    return encoded_string
def char_to_int(char):
    # Ensure the character is uppercase
    char = char.upper()
    # Convert the character to an integer (A -> 1, B -> 2, ..., Z -> 26)
    return ord(char) - ord('A') + 1
def string_to_int_small(s):
    # Ensure the string is a digit and within the range 0-9
    if s.isdigit() and 0 <= int(s) <= 9:
        # Convert the string to an integer (0 -> 30, 1 -> 31, ..., 9 -> 39)
        return ord(s) - ord('0') + 30
    else:
        raise ValueError("Input should be a digit between '0' and '9'")
def string_to_int_Big(s):
    # Ensure the string is a digit and within the range 0-9
    if s.isdigit() and 0 <= int(s) <= 9:
        # Convert the string to an integer (0 -> 30, 1 -> 31, ..., 9 -> 39)
        return ord(s) - ord('0') + 40
    else:
        raise ValueError("Input should be a digit between '0' and '9'")
def string_to_int_Big(s):
    # Ensure the string is a digit and within the range 0-9
    if s.isdigit() and 0 <= int(s) <= 9:
        # Convert the string to an integer (0 -> 30, 1 -> 31, ..., 9 -> 39)
        return ord(s) - ord('0') + 40
    else:
        raise ValueError("Input should be a digit between '0' and '9'")
def refreshCarSlot(current_ip):
    cams = getIpCams()
    for cam in cams:
        ip = cam["ip"]
        in_out = cam["in_out"]
        if current_ip != ip:
            cam_status[ip].heartbeatToSend["0"].clear()
            cam_status[ip].heartbeatToSend["1"].clear()
            cam_status[ip].serialDataToSend["0"].clear()
            cam_status[ip].serialDataToSend["1"].clear()
            if in_out == '0' and len(cam_status[ip].carQueue) <=0:
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["1"])
                setCarSlotsSmall(ip)
                setCarSlotsBig(ip)
            elif in_out == '1' and len(cam_status[ip].carQueue) <=0:
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["1"])
                setOutNormalScreen(ip)
                setCarSlotsBig(ip)
def led_init():
    cams = getIpCams()
    for cam in cams:
        ip = cam["ip"]
        in_out = cam["in_out"]
        setCams(ip)
        if len(cam_status[ip].heartbeatToSend["0"]) <=0 and len(cam_status[ip].heartbeatToSend["1"]) <=0 and len(cam_status[ip].serialDataToSend["0"]) <=0 and len(cam_status[ip].serialDataToSend["0"]) <=0:
            if in_out == '0' and len(cam_status[ip].carQueue) <=0:
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["1"])
                setCarSlotsSmall(ip)
                setCarSlotsBig(ip)
            elif in_out == '1' and len(cam_status[ip].carQueue) <=0:
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["0"])
                cleanLEDSerialData(cam_status[ip].heartbeatToSend["1"])
                setOutNormalScreen(ip)
                setCarSlotsBig(ip)
def led_refresh():
    while(True):
        time.sleep(5)
        led_init()
def run(server_class=http.server.HTTPServer, handler_class=MyHandler, port=8081):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd on port %d...", port)
    httpd.serve_forever()
    
#initialize variables
url = 'http://192.168.0.252:8080/function.php'
pic_dir = "/storage/sdcard/Cars"
backup_dir = "/storage/sdcard/Cars_backup"
os.makedirs(pic_dir, exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)

nowTime = datetime.now()
cam_status = {}
led_init()
if __name__ == "__main__":
    threading.Thread(target=led_refresh).start()
    run()