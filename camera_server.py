import http.server
import json
import logging
import requests
import base64
import os
from datetime import datetime, timedelta
import time
import threading
import shutil
class camStatus:
    def __init__(self):
        self.needToOpen = False
        self.needToClose = False
        self.serialDataToSend = {"0":[], "1":[]} #Data Queue to send to LED by serialdata
        self.carQueue = [] #Car Info Queue waiting for gio
        self.carGio0 = 1 #Camera  Gio0 status
        self.carGio1 = 1 #Camera  Gio1 status
        self.refreshCarSlotBoolean = True
        self.imageOpen = False
        self.carFullQueue = []
        self.serialStop = False
        
class MyHandler(http.server.BaseHTTPRequestHandler):
    global cam_status
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
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except:
            print(response)
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
        for i in range(0, 50):
            time.sleep(0.2)
            if in_out == "0":
                if cam_status[ip].carGio0 == 0:
                    cam_status[ip].carQueue.append(data)
                    cam_status[ip].needToOpen = True
                    threading.Thread(target=self.waitForGio1Triggered, args=(in_out, ip,)).start()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    setWelcomeSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                    break
            else:
                if cam_status[ip].carGio0 == 0:
                    cam_status[ip].needToOpen = True
                    cam_status[ip].carQueue.append(data)
                    threading.Thread(target=self.waitForGio1Triggered, args=(in_out, ip,)).start()
                    #set thank u to XXXXXXX
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    setThankUSerialData(ip)
                    setCarNumberSerialData(ip, car_number)
                    break
    def waitForGio1Triggered(self, in_out, ip):
        needPop = True
        for i in range(0, 50):
            time.sleep(0.2)
            if in_out == "0":
                if cam_status[ip].carGio1 == 0:
                    updateCarInside(ip)
                    #set LED0 and LED1 to slot left
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                    setCarSlotsBig(ip)
                    setCarSlotsSmall(ip)
                    needPop = False
                    # refreshCarSlot(ip)
                    break
            else:
                if cam_status[ip].carGio1 == 0:
                    updateHistory(ip)
                    #set LED0 to pay before leave and LED1 to slot left
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                    setCarSlotsBig(ip)
                    setOutNormalScreen(ip)
                    needPop = False
                    # refreshCarSlot(ip)
                    break
        # GIO1 not triggered, dispose data
        if needPop:
            # cam_status[ip].needToClose = True
            cam_status[ip].carQueue.pop(0)
    def waitForGio1NotTriggered(self, ip):
        needPop = True
        for i in range(0, 50):
            time.sleep(0.2)
            if cam_status[ip].carGio1 == 0:
                needPop = False
        # GIO1 not triggered, dispose data
        if needPop:
            cam_status[ip].needToClose = True
    def waitForBothGioNotTriggered(self, ip):
        needClose = False
        while(needClose == False and cam_status[ip].imageOpen == True):
            needClose = True
            for i in range(0, 50):
                time.sleep(0.2)
                if cam_status[ip].imageOpen == False:
                    break
                if cam_status[ip].carGio1 == 0 or cam_status[ip].carGio0 == 0:
                    cam_status[ip].imageOpen = True
                    needClose = False
                    break
        # GIO1 not triggered, dispose data
        if needClose == True:
            if cam_status[ip].imageOpen == True:
                cam_status[ip].needToClose = True
                cam_status[ip].imageOpen = False
            cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
            setCarSlotsSmall(ip)
            setCarSlotsSmall(ip)
    #handle heartbeat request and return a response json for heartbeat
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
        if "open" in cam:
            open = cam["open"]
            #update cam with gate close
            updateCamNotToOpen(ip)
        #check if need to close the gate from SQL database
        if "close" in cam:
            close = cam["close"]
            if close == "1":
                updateCamNotToClose(ip)
        
        if len(cam_status[ip].carFullQueue) > 0 and checkCanIn():
            data = cam_status[ip].carFullQueue.pop()
            reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
            car_number = reselt["license"]
            cam_status[ip].carQueue.append(data)
            updateCarInside(ip)
            cam_status[ip].refreshCarSlotBoolean = False
            if cam_status[ip].imageOpen == False:
                cam_status[ip].imageOpen = True
                threading.Thread(target=self.waitForBothGioNotTriggered, args=(ip,)).start()
            cam_status[ip].serialDataToSend["0"].clear()
            cam_status[ip].serialDataToSend["1"].clear()
            cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
            cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
            displayWelcomeThreeTimes(ip, car_number)
            cam_status[ip].needToOpen = True
        cam_status[ip].needToOpen = cam_status[ip].needToOpen or open == "1"
        #open the gate with json info = "ok"
        if cam_status[ip].needToOpen:
            if cam_status[ip].serialStop:
                cam_status[ip].needToOpen = False
                cam_status[ip].serialStop = False
                res["Response_Heartbeat"]["info"] = "ok"
            else:
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 0,
                    "data": "",
                    "dataLen": 0
                })
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 1,
                    "data": "",
                    "dataLen": 0
                })
                cam_status[ip].serialStop = True
            return res
        cam_status[ip].needToClose = cam_status[ip].needToClose or close == "1"
        #close the gate with json shutoff = "ok
        if cam_status[ip].needToClose:
            if cam_status[ip].serialStop:
                cam_status[ip].needToClose = False
                cam_status[ip].serialStop = False
                res["Response_Heartbeat"]["shutoff"] = "ok"
            else:
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 0,
                    "data": "",
                    "dataLen": 0
                })
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 1,
                    "data": "",
                    "dataLen": 0
                })
                cam_status[ip].serialStop = True
            return res
        #check if heartbeat has serial data
        if ip in cam_status:
            if len(cam_status[ip].serialDataToSend["0"]) > 0:
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 0,
                    "data": cam_status[ip].serialDataToSend["0"][0],
                    "dataLen": 38
                })
            if len(cam_status[ip].serialDataToSend["1"]) > 0:
                res["Response_Heartbeat"]["serialData"].append({
                    "serialChannel": 1,
                    "data": cam_status[ip].serialDataToSend["1"][0],
                    "dataLen": 38
                })
        if len(cam_status[ip].serialDataToSend["0"]) <= 0 and len(cam_status[ip].serialDataToSend["1"]) <= 0 and cam_status[ip].refreshCarSlotBoolean ==False and cam_status[ip].imageOpen == False:
                cam_status[ip].refreshCarSlotBoolean = True
        return res
    #handle gio request and return reponse json for Gio
    def handleGioData(self, data):
        ip = data["AlarmGioIn"]["ipaddr"]
        serial_num = data["AlarmGioIn"]["result"]["TriggerResult"]["source"]
        serial_value = data["AlarmGioIn"]["result"]["TriggerResult"]["value"]
        
        cam = getIpCam(ip)
        if cam is None:
            return ""
        if serial_num == 0:
            original = cam_status[ip].carGio0
            cam_status[ip].carGio0 = serial_value
            if original==0 and serial_value==1:
                cam_status[ip].carFullQueue.clear()
        else:
            original = cam_status[ip].carGio1
            cam_status[ip].carGio1 = serial_value
            if original==0 and serial_value==1 and cam_status[ip].imageOpen == True:
                cam_status[ip].imageOpen = False
        return ""
    #handle Serial request and return reponse json for Serial
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
            if cam_status[ip].needToOpen:
                cam_status[ip].serialStop = True
                return res
            else:
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
                if len(cam_status[ip].serialDataToSend["0"]) <= 0 and len(cam_status[ip].serialDataToSend["1"]) <= 0 and cam_status[ip].refreshCarSlotBoolean ==False and cam_status[ip].imageOpen == False:
                    cam_status[ip].refreshCarSlotBoolean = True
        return res
    # handle AlarmInfoPlate request from ip-cam, and return a response
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
        if car_number == 'No Plate' or car_number == "":
            addLogs(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), "辨識不到車牌")
            return response
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
        cam_status[ip].refreshCarSlotBoolean = False
        #check the cam is in or out
        if cam_in_out == "0":
            #in-cam
            if checkCanIn():
                addLogs(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), car_number + "進場")
                #if the car is allowed to in, refresh the LED and add it to the database.
                if read_gio == '1':
                    if cam_status[ip].imageOpen == False:
                        cam_status[ip].imageOpen = True
                        threading.Thread(target=self.waitForBothGioNotTriggered, args=(ip,)).start()
                    cam_status[ip].carQueue.append(data)
                    updateCarInside(ip)
                    # threading.Thread(target=self.waitForGio1NotTriggered, args=(ip,)).start()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                    # response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    # response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    # response["Response_AlarmInfoPlate"]["serialData"][1]["data"] = getCleanLEDSerialData()
                    # response["Response_AlarmInfoPlate"]["serialData"][1]["dataLen"] = 38
                    displayWelcomeThreeTimes(ip, car_number)
                else:
                    # if cam_status[ip].carGio0 != 0:
                    #     #gio0 in is not triggered
                    #     threading.Thread(target=self.waitForGio0Triggered, args=(cam_in_out, data, ip, car_number)).start()
                    #     return response
                    if cam_status[ip].imageOpen == False:
                        cam_status[ip].imageOpen = True
                        threading.Thread(target=self.waitForBothGioNotTriggered, args=(ip,)).start()
                    cam_status[ip].carQueue.append(data)
                    threading.Thread(target=self.waitForGio1Triggered, args=(cam_in_out, ip,)).start()
                    # add serial0 data to WELCOME XXXXXXX
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    displayWelcomeThreeTimes(ip, car_number)
                response["Response_AlarmInfoPlate"]["info"] = "no"
                cam_status[ip].needToOpen = True
            else:
                addLogs(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), "車位已滿")
                cam_status[ip].serialDataToSend["0"].clear()
                cam_status[ip].serialDataToSend["1"].clear()
                response["Response_AlarmInfoPlate"]["info"] = "no"
                #add serial0 data to full and wait
                response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                setCarSlotsSmall(ip)
                cam_status[ip].carFullQueue.append(data)
        else:
            #out cam
            if checkCanOut(data):
                addLogs(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), car_number + "出場")
                #if the car is allowed to out, refresh the LED and add it to the database.
                if read_gio == '1':
                    if cam_status[ip].imageOpen == False:
                        cam_status[ip].imageOpen = True
                        threading.Thread(target=self.waitForBothGioNotTriggered, args=(ip,)).start()
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    cam_status[ip].carQueue.append(data)
                    updateHistory(ip)
                    # threading.Thread(target=self.waitForGio1NotTriggered, args=(ip,)).start()
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                    # response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    # response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    # response["Response_AlarmInfoPlate"]["serialData"][1]["data"] = getCleanLEDSerialData()
                    # response["Response_AlarmInfoPlate"]["serialData"][1]["dataLen"] = 38
                    displayThankUThreeTimes(ip, car_number)
                    # setOutNormalScreen(ip)
                else:
                    # if cam_status[ip].carGio0 != 0:
                    #     #gio0 out is not triggered
                    #     threading.Thread(target=self.waitForGio0Triggered, args=(cam_in_out, data, ip, car_number)).start()
                    #     return response
                    if cam_status[ip].imageOpen == False:
                        cam_status[ip].imageOpen = True
                        threading.Thread(target=self.waitForBothGioNotTriggered, args=(ip,)).start()
                    cam_status[ip].carQueue.append(data)
                    threading.Thread(target=self.waitForGio1Triggered, args=(cam_in_out, ip,)).start()
                    #set thank u to XXXXXXX
                    response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                    response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                    cam_status[ip].serialDataToSend["0"].clear()
                    cam_status[ip].serialDataToSend["1"].clear()
                    displayThankUThreeTimes(ip)
                    setCarNumberSerialData(ip, car_number)
                response["Response_AlarmInfoPlate"]["info"] = "no"
                cam_status[ip].needToOpen = True
            else:
                #if the car is not allowed to out, show need-to-play on LED
                cam_status[ip].serialDataToSend["0"].clear()
                cam_status[ip].serialDataToSend["1"].clear()
                response["Response_AlarmInfoPlate"]["info"] = "no"
                #add serial0 data to need to pay
                response["Response_AlarmInfoPlate"]["serialData"][0]["data"] = getCleanLEDSerialData()
                response["Response_AlarmInfoPlate"]["serialData"][0]["dataLen"] = 38
                displayNeedToPayThreeTimes(ip, car_number)
        return response
    
def displayWelcomeThreeTimes(ip, car_number):
    for i in range(0,3):
        setWelcomeSerialData(ip)
        setCarNumberSerialData(ip, car_number)
        
def displayThankUThreeTimes(ip, car_number):
    for i in range(0,3):
        setThankUSerialData(ip)
        setCarNumberSerialData(ip, car_number)
def displayNeedToPayThreeTimes(ip, car_number):
    for i in range(0,3):
        setNeedToPay(ip)
        setCarNumberSerialData(ip, car_number)  
#update database after car go in
def updateCarInside(ip):
    data = cam_status[ip].carQueue.pop(0)
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    size = "0"
    color = reselt["carColor"]
    car_number = reselt["license"]
    
    if isCarInside(car_number) == True:
        index = 1
        car_number = reselt["license"] + '-' + str(index)
        while(isCarInside(car_number) == True):
            index = index + 1
            car_number = reselt["license"] + '-' + str(index)
    if not os.path.exists(pic_dir):
        os.makedirs(pic_dir, exist_ok=True)
    file_name = pic_dir + "/" + car_number + ".png"
    if "imageFile" in reselt:
        image_string = reselt["imageFile"]
        #add new car and open gate
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, "wb") as fh:
            fh.write(base64.decodebytes(str.encode(image_string)))
        addCarInside(car_number, "A", file_name, size, color)
#update database after car go out
def updateHistory(ip):
    nowTime = datetime.now()
    data = cam_status[ip].carQueue.pop(0)
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    car_number = reselt["license"]
    file_name = pic_dir + "/" + car_number + ".png"
    backup_file_name = getBackUpDirectory() + "/" + nowTime.strftime("%Y_%m_%d_%H_%M_%S") + "_" + car_number
    carInside = getCarInside(car_number)
    #upload a car history to database
    addHistory(carInside, nowTime.strftime("%Y-%m-%d %H:%M:%S"), backup_file_name)
    #delete the car in car_inside table on database
    deleteCarInside(car_number)
    
    if "imageFile" in reselt:
        image_string = reselt["imageFile"]
        #move car_inside picture to history folder
        if os.path.exists(file_name):
            shutil.move(file_name, backup_file_name + "_in.png")
        #add car out picture to history folder
        with open(backup_file_name+ "_out.png", "wb") as fh:
            fh.write(base64.decodebytes(str.encode(image_string)))
#get the path back-up pic should be stored
def getBackUpDirectory():
    year_dir = backup_dir + '/' + nowTime.strftime("%Y")
    month_dir = year_dir + '/' + nowTime.strftime("%m")
    day_dir = month_dir + '/' +  nowTime.strftime("%d")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    if not os.path.exists(year_dir):
        os.makedirs(year_dir, exist_ok=True)
    if not os.path.exists(month_dir):
        os.makedirs(month_dir, exist_ok=True)
    if not os.path.exists(day_dir):
        os.makedirs(day_dir, exist_ok=True)
    return day_dir
#check the car can enter(check slots and cars_inside)
def checkCanIn():
    ret = False
    # carInside = getCarInside(car_number)
    available = slotSearch()
    if available > 0:
        ret = True
    return ret
#check the car can exit(check paytime)
def checkCanOut(data):
    ret = False
    #car detailed data
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    car_number = reselt["license"]
    if car_number == 'No Plate' or car_number == "":
        return ret
    carInside = getCarInside(car_number)
    if carInside is not None:
        nowTime = datetime.now()
        regular_pass = checkIsRegular(car_number)
        if regular_pass is not None and regular_pass['due_date'] is not None:
            due_time = datetime.strptime(regular_pass['due_date'], "%Y-%m-%d")
            due_time = due_time + timedelta(days=1)
            if due_time >= nowTime:  
                return True
            else:
                addLogs(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), "月租車過期:"+car_number)
        elif carInside["time_pay"] is not None and carInside["time_pay"] != "":
            time_pay = carInside["time_pay"]
            payTime = datetime.strptime(time_pay, "%Y-%m-%d %H:%M:%S")
            diffTime = nowTime-payTime
            seconds = diffTime.seconds
            if seconds <= getExitCountTime():
                ret = True
        else:
            addLogs(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), "車輛尚未繳費:"+car_number)
    else:
        addLogs(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), "場內無此車:"+car_number)
    return ret
#check if the car is a regular car
def checkIsRegular(carNumber):
    #get total cat slots
    myobj = {'func': 'regular_pass_single_search', 'car_number':carNumber}
    x = requests.get(url, params = myobj)
    try:
        data = json.loads(x.text)
        if len(data) > 0:
            data = list(data)
            regular_data = data[0]
            return regular_data
    except json.JSONDecodeError:
        return None
#check available slots
def getExitCountTime():
    ret = 900
    myobj = {'func': 'fee_search'}
    x = requests.get(url, params = myobj)
    try:
        data = json.loads(x.text)
        if len(data) > 0:
            data = list(data)
            fee_data = data[0]
            return int(fee_data['enter_time_not_count']) * 60
        else:
            return 900
    except json.JSONDecodeError:
        return 900
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
            slot = slot - int(slot_data['reserved_slot'])
            slot = slot + int(slot_data['car_left'])
            slot = slot + int(slot_data['pregnant_left'])
            slot = slot + int(slot_data['charging_left'])
            slot = slot + int(slot_data['disabled_left'])
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
    if myobj["time_pay"] is None:
        myobj["time_pay"] = time_out
    myobj["cost"] = car_data["cost"]
    if myobj["cost"] is None:
        myobj["cost"] = 0
    myobj["bill_number"] = car_data["bill_number"]
    if myobj["bill_number"] is None:
        myobj["bill_number"] = "None"
    myobj["payment"] = car_data["payment"]
    if myobj["payment"] is None:
        myobj["payment"] = "R"
    myobj["artificial"] = car_data["artificial"]
    myobj["type"] = car_data["type"]
    myobj["color"] = car_data["color"]
    myobj["path"] = path
    x = requests.post(url + "?func=history_add", data = myobj)
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
#set ip cam close=0 after open on backend app
def updateCamNotToClose(ip):
    #update cam close status on SQL
    myobj = {'func': 'cam_update_close'}
    myobj["ip"] = ip
    myobj["close"] = 0
    x = requests.get(url, params = myobj)
#add log to database
def addLogs(time, description):
    #update cam open status on SQL
    myobj = {'func': 'server_history_add'}
    myobj["time"] = time
    myobj["description"] = description
    x = requests.post(url + "?func=server_history_add", data = myobj)
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
    cam_status[ip].serialDataToSend["0"].append(getBase64String(serial_data))
#clear LED
def cleanLEDSerialData(array):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3C ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    array.append(getBase64String(serial_data))
#clear LED
def getCleanLEDSerialData():
    # serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3C ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    serial_data = bytearray([0xAA ,0xA5 ,0x08 ,0x00 ,0xFF ,0xFF ,0x00 ,0x00 ,0xB0 ,0xA1 ,0x00 ,0x02 ,0x00 ,0x00 ,0x5A ,0x55])

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
def led_refresh_loop():
    cams = getIpCams()
    if len(cams) != len(cam_status):
        for cam in cams:
            setCams(cam["ip"])
    for cam in cams:
        ip = cam["ip"]
        in_out = cam["in_out"]
        if len(cam_status[ip].carQueue) <=0 and cam_status[ip].refreshCarSlotBoolean == True:
            cam_status[ip].serialDataToSend["0"].clear()
            cam_status[ip].serialDataToSend["1"].clear()
            if in_out == '0':
                cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                setCarSlotsSmall(ip)
                setCarSlotsSmall(ip)
                setCarSlotsBig(ip)
                setCarSlotsBig(ip)
            elif in_out == '1':
                cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                setOutNormalScreen(ip)
                setOutNormalScreen(ip)
                setCarSlotsBig(ip)
                setCarSlotsBig(ip)
def refreshCarSlot(current_ip):
    cams = getIpCams()
    for cam in cams:
        ip = cam["ip"]
        in_out = cam["in_out"]
        if current_ip != ip:
            if len(cam_status[ip].carQueue) <=0 and cam_status[ip].refreshCarSlotBoolean == True and len(cam_status[ip].serialDataToSend["0"]) == 0 and len(cam_status[ip].serialDataToSend["1"]) == 0:
                if in_out == '0':
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                    setCarSlotsSmall(ip)
                    setCarSlotsBig(ip)
                elif in_out == '1':
                    cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                    cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                    setOutNormalScreen(ip)
                    setCarSlotsBig(ip)
def led_init():
    cams = getIpCams()
    for cam in cams:
        ip = cam["ip"]
        in_out = cam["in_out"]
        setCams(ip)
        if len(cam_status[ip].carQueue) <=0 and cam_status[ip].refreshCarSlotBoolean == True:
            if in_out == '0':
                cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                setCarSlotsSmall(ip)
                setCarSlotsBig(ip)
            elif in_out == '1':
                cam_status[ip].serialDataToSend["0"].append(getCleanLEDSerialData())
                cam_status[ip].serialDataToSend["1"].append(getCleanLEDSerialData())
                setOutNormalScreen(ip)
                setCarSlotsBig(ip)
#update LED with slots every 8 seconds
def led_refresh():
    while(True):
        time.sleep(8)
        led_refresh_loop()
def run(server_class=http.server.HTTPServer, handler_class=MyHandler, port=8081):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd on port %d...", port)
    threading.Thread(target=led_refresh).start()
    httpd.serve_forever()
    
#initialize variables
url = 'http://192.168.1.200:8080/function.php'
pic_dir = "/storage/sd-ext/Cars/"
backup_dir = "/storage/sd-ext/Cars_backup"
# os.makedirs(pic_dir, exist_ok=True)
# os.makedirs(backup_dir, exist_ok=True)
keepTry = True
while(keepTry == True):
    time.sleep(1)
    try:
        myobj = {'func': 'cam_search'}
        x = requests.get(url, params = myobj)
        keepTry = False
    except:
        print("Can't connect to the server.")

nowTime = datetime.now()
cam_status = {}

led_init()
if __name__ == "__main__":
    run()