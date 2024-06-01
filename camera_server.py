import http.server
import json
import logging
import requests
import base64
import os
from datetime import datetime

class IpCam:
    name = ""
    ip = ""
    in_out = False
    pay = False
    open = False
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
        post_data = self.rfile.read(content_length)
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
            response = check_car(data)
            # res = {
		    # "Response_AlarmInfoPlate": {
			#     "info": "ok",
			#     "content": "retransfer_stop",
			#     "is_pay": "true",
			#     "serialData": []
		    #     }
	        # }
        elif "heartbeat" in data:
            response = {"status": "received"}
        elif "AlarmGioIn" in data:
            response = {"status": "received"}
        elif "SerialData" in data:
            response = {"status": "received"}
        
        return response
def check_car(data):
    #car detailed data
    reselt = data["AlarmInfoPlate"]["result"]["PlateResult"]
    ip = data["AlarmInfoPlate"]["ipaddr"]
    size = "0"
    color = reselt["carColor"]
    image_string = reselt["imageFile"]
    car_number = reselt["license"]
    file_name = "/storage/sdcard/Cars/" + car_number + ".png"
    # response for picture
    res ={
        "Response_AlarmInfoPlate": {
            "info": "ok",
            "content": "retransfer_stop",
            "is_pay": "true",
            "serialData": []
            }
        }
    # if os.path.exists(file_name):
    #     os.remove(file_name)
    # else:
    #     with open(file_name, "wb") as fh:
    #         fh.write(base64.decodebytes(str.encode(image_string)))
    # get ip cam data
    cam = getIpCam(ip)
    cam_in_out = 0
    if("in_out" in cam):
        cam_in_out = cam["in_out"]
    carInside = getCarInside(car_number)
    if cam_in_out == "0":
        available = slotSearch()
        if available > 0 and carInside is None:
            #add new car and open gate
            if os.path.exists(file_name):
                os.remove(file_name)
            with open(file_name, "wb") as fh:
                fh.write(base64.decodebytes(str.encode(image_string)))
            addCarInside(car_number, "A", file_name, size, color)
            #add serial0 data to WELCOME XXXXXXX
            setWelcomeSerialData(ip)
            setCarNumberSerialData(ip, car_number, "0")
            #add serial1 data to update slots number
            setCarSlotsBig()
        else:
            res["Response_AlarmInfoPlate"]["info"] = "no"
            #add serial0 data to full and wait
            setCarSlotsSmall(0)
    else:
        # if carInside is not None:
        #     deleteCarInside(car_number)
        #     if os.path.exists(file_name):
        #         os.remove(file_name)
        if carInside is not None and carInside["time_pay"] is not None:
            time_pay = carInside["time_pay"]
            nowTime = datetime.now()
            payTime = datetime.strptime(time_pay, "%Y-%m-%d %H:%M:%S")
            diffTime = nowTime-payTime
            seconds = diffTime.seconds
            if seconds <= 900:
                #close gate and show no available car slot
                addHistory(carInside, nowTime)
                deleteCarInside(car_number)
                if os.path.exists(file_name):
                    os.remove(file_name)
                #add serial0 data to THANK U XXXXXXX
                setThankUSerialData(ip)
                setCarNumberSerialData(ip, car_number, "0")
                #add serial1 data to update slots number
            else:
                res["Response_AlarmInfoPlate"]["info"] = "no"
                #add serial0 data to need to pay
                setNeedToPay(ip)
        else:
            res["Response_AlarmInfoPlate"]["info"] = "no"
    return res
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

def isCarInside(car_number):
    data = getCarInside(car_number)

    if data is not None:
        return True
    else:
        return False
    
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
    
def deleteCarInside(car_number):
    myobj = {'func': 'cars_inside_delete'}
    myobj["car_number"] = car_number
    x = requests.get(url, params = myobj)

def addHistory(car_data, time_out):
    myobj = {'func': 'cars_inside_delete'}
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
    x = requests.get(url, params = myobj)
    
def getIpCam(ip):
    myobj = {'func': 'cam_single_search'}
    myobj["ip"] = ip
    x = requests.get(url, params = myobj)
    data = json.loads(x.text)

    if len(data) > 0:
        data = list(data)
        cam = data[0]
        setCams(ip)
        return cam
    else:
        return None
def setCams(ip):
    if ip not in serialDataToSend:
        serialDataToSend[ip]={
            "0":[],
            "1":[]
        }
   
def setWelcomeSerialData(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    if ip not in serialDataToSend:
        serialDataToSend[ip] ={}
    if "0" not in serialDataToSend[ip]:
        serialDataToSend[ip]["0"] = []
    serialDataToSend[ip]["0"].append(getBase64String(serial_data))
    
    
def setCarNumberSerialData(ip, car_number, port):
    for i in range(len(car_number)):
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x10 ,0x00 ,0x08 ,0x00 ,0x10 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x01 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        serial_data[12] = i*8
        if car_number[i].isdigit():
            serial_data[32] = string_to_int_small(car_number[i])
        else:
            serial_data[32] = char_to_int(car_number[i])
        if ip not in serialDataToSend:
            serialDataToSend[ip] ={}
        if "0" not in serialDataToSend[ip]:
            serialDataToSend[ip][port] = []
        serialDataToSend[ip][port].append(getBase64String(serial_data))
        
def setThankUSerialData(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x37 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    if ip not in serialDataToSend:
        serialDataToSend[ip] ={}
    if "0" not in serialDataToSend[ip]:
        serialDataToSend[ip]["0"] = []
    serialDataToSend[ip]["0"].append(getBase64String(serial_data))
        
def setCarSlotsBig(number):
    P_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x14 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x32 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    for ip in serialDataToSend:
        serialDataToSend[ip]["0"].append(getBase64String(P_data))
    if number > 0:
        format_number = '{:03d}'.format(number)
        for i in range(len(format_number)):
            serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
            serial_data[12] = 20+i*14
            serial_data[32] = string_to_int_Big(format_number[i])
            for ip in serialDataToSend:
                serialDataToSend[ip]["0"].append(getBase64String(serial_data))
    else:
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x14 ,0x00 ,0x00 ,0x00 ,0x2A ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x33 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        serialDataToSend[ip]["0"].append(getBase64String(serial_data))
def setCarSlotsSmall(ip, number):
    if number > 0:
        P_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x12 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x35 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        serialDataToSend[ip]["0"].append(getBase64String(P_data))
        format_number = '{:03d}'.format(number)
        for i in range(len(format_number)):
            serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x10 ,0x00 ,0x08 ,0x00 ,0x10 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x36 ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
            serial_data[12] = 20+i*8
            serial_data[32] = string_to_int_small(format_number[i])
            serialDataToSend[ip]["0"].append(getBase64String(serial_data))
    else:
        serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3D ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
        serialDataToSend[ip]["0"].append(getBase64String(serial_data))
def setNeedToPay(ip):
    serial_data = bytearray([0xaa,0xa5,0x1e,0x00,0x01,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x02 ,0x00 ,0x00 ,0x00 ,0x00 ,0x40 ,0x00 ,0x20 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x02 ,0x00 ,0x00 ,0x00 ,0x3E ,0x00 ,0x00 ,0x00 ,0x5a ,0x55])
    serialDataToSend[ip]["0"].append(getBase64String(serial_data))
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

def run(server_class=http.server.HTTPServer, handler_class=MyHandler, port=8081):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd on port %d...", port)
    httpd.serve_forever()
    
url = 'http://localhost:8080/function.php'
serialDataToSend = {}
if __name__ == "__main__":
    run()