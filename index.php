<?php
//require_once('conn.php');
$AlarmInfoPlate = "AlarmInfoPlate";
$AlarmGioIn = "AlarmGioIn";
$SerialData = "SerialData";
$heartbeat = "heartbeat";

$data = json_decode(file_get_contents('php://input'), true);
header('Content-Type: application/json; charset=utf-8');
if (isset($data[$AlarmInfoPlate])){
	echo '{
		"Response_AlarmInfoPlate": {
			"info": "ok",
			"content": "retransfer_stop",
			"is_pay": "true",
			"serialData": []
		}
	}';
}else if (isset($data[$AlarmGioIn])){
	echo "false";
}else if (isset($data[$SerialData])){
	echo "false";
}else if (isset($data[$heartbeat])){
	echo "false";
}


?>