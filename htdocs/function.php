<?php
require_once('conn.php');




function slotUpdate($query)
{
    $car = 0;
    $pregnant = 0;
    $disabled = 0;
    $charging = 0;
    $reserved = 0;
    if (!empty($_GET['car'])) {
        $car = $_GET['car'];
    }
    ;
    if (!empty($_GET['pregnant'])) {
        $pregnant = $_GET['pregnant'];
    }
    ;
    if (!empty($_GET['disabled'])) {
        $disabled = $_GET['disabled'];
    }
    ;
    if (!empty($_GET['charging'])) {
        $charging = $_GET['charging'];
    }
    ;
    if (!empty($_GET['reserved'])) {
        $reserved = $_GET['reserved'];
    }
    ;
    $query = sprintf(
        "UPDATE floor SET car_slot = '%d', pregnant_slot = '%d', disabled_slot = '%d', charging_slot = '%d', reserved_slot = '%d' WHERE floor.id = 1",
        $car,
        $pregnant,
        $disabled,
        $charging,
        $reserved
    );
    return $query;
}
function feeUpdate($query)
{
    $query = sprintf(
        "UPDATE basic_fee SET enter_time_not_count = '%d', before_one_hour_count = '%d', after_one_hour_unit = '%d', weekday_fee = '%d', weekday_most_fee = '%d', holiday_fee = '%d', holiday_most_fee = '%d', weekday_holiday_cross = '%d' WHERE basic_fee.id = 1",
        $_GET['enter_time_not_count'],
        $_GET['before_one_hour_count'],
        $_GET['after_one_hour_unit'],
        $_GET['weekday_fee'],
        $_GET['weekday_most_fee'],
        $_GET['holiday_fee'],
        $_GET['holiday_most_fee'],
        $_GET['weekday_holiday_cross'],
    );
    return $query;
}
function company_info_Update($query)
{
    $query = sprintf(
        "UPDATE company_info SET lot_name = '%s', company_name = '%s', company_address = '%s', company_phone = '%s', server_token = '%s', cht_chat_id = '%s', standby_path = '%s', standby_sec = '%d', auto_upload_server = '%d', standby_play = '%d' WHERE company_info.id = 1",
        $_GET['lot_name'],
        $_GET['company_name'],
        $_GET['company_address'],
        $_GET['company_phone'],
        $_GET['server_token'],
        $_GET['cht_chat_id'],
        $_GET['standby_path'],
        $_GET['standby_sec'],
        $_GET['auto_upload_server'],
        $_GET['standby_play']
    );
    return $query;
}
function userSingleSearch($query)
{
    $account = '';
    $password = '';
    if (!empty($_GET['account'])) {
        $account = $_GET['account'];
    }
    if (!empty($_GET['password'])) {
        $password = $_GET['password'];
    }
    $query = sprintf(
        "SELECT * FROM user WHERE account='%s' AND password='%s'",
        $account,
        $password
    );

    return $query;
}
function userDelete($query)
{
    $account = '';
    if (!empty($_GET['account'])) {
        $account = $_GET['account'];
    } else {
        return '';
    }
    $query = sprintf(
        "DELETE FROM user WHERE account='%s'",
        $account
    );
    return $query;
}
function userUpdate($query)
{
    $account = '';
    $name = '';
    $phone = '';
    $permission = '';
    $account = '';
    if (!empty($_GET['account'])) {
        $account = $_GET['account'];
    }
    if (!empty($_GET['password'])) {
        $password = $_GET['password'];
    }
    if (!empty($_GET['name'])) {
        $name = $_GET['name'];
    }
    if (!empty($_GET['phone'])) {
        $phone = $_GET['phone'];
    }
    if (!empty($_GET['permission'])) {
        $permission = $_GET['permission'];
    }
    $query = sprintf(
        "UPDATE user SET password = '%s', name = '%s', phone = '%s', permission = '%s' WHERE account = '%s'",
        $password,
        $name,
        $phone,
        $permission,
        $account
    );
    return $query;
}
function userAdd($query)
{
    $account = '';
    $name = '';
    $phone = '';
    $permission = '';
    $account = '';
    if (!empty($_GET['account'])) {
        $account = $_GET['account'];
    }
    if (!empty($_GET['password'])) {
        $password = $_GET['password'];
    }
    if (!empty($_GET['name'])) {
        $name = $_GET['name'];
    }
    if (!empty($_GET['phone'])) {
        $phone = $_GET['phone'];
    }
    if (!empty($_GET['permission'])) {
        $permission = $_GET['permission'];
    }
    $query = sprintf(
        "INSERT INTO user (account,password,name,phone,permission)
        VALUES ('%s', '%s', '%s','%s','%s');",
        $account,
        $password,
        $name,
        $phone,
        $permission
    );
    return $query;
}
function userPasswordChange($query)
{
    $account = '';
    $password = '';
    if (!empty($_GET['account'])) {
        $account = $_GET['account'];
    }
    if (!empty($_GET['password'])) {
        $password = $_GET['password'];
    }
    $query = sprintf(
        "UPDATE `user` SET `password` = '%s' WHERE `account` = '%s'",
        $password,
        $account
    );
    return $query;
}
function camSingleSearch($query)
{
    $ip = '';
    if (!empty($_GET['ip'])) {
        $ip = $_GET['ip'];
    }
    $query = sprintf(
        "SELECT * FROM ip_cam WHERE ip='%s'",
        $ip
    );

    return $query;
}

function camDelete($query)
{
    $ip = '';
    if (!empty($_GET['ip'])) {
        $ip = $_GET['ip'];
    } else {
        return '';
    }
    $query = sprintf(
        "DELETE FROM ip_cam WHERE ip='%s'",
        $ip
    );
    return $query;
}
function camAdd($query)
{
    $ip = '';
    $name = '';
    $in_out = '';
    $pay = '';
    $read_gio = '';
    if (!empty($_GET['ip'])) {
        $ip = $_GET['ip'];
    }
    if (!empty($_GET['name'])) {
        $name = $_GET['name'];
    }
    if (!empty($_GET['number'])) {
        $number = $_GET['number'];
    }
    if (!empty($_GET['in_out'])) {
        $in_out = $_GET['in_out'];
    }
    if (!empty($_GET['pay'])) {
        $pay = $_GET['pay'];
    }
    if (!empty($_GET['read_gio'])) {
        $read_gio = $_GET['read_gio'];
    }
    $query = sprintf(
        "INSERT INTO ip_cam (number,name,ip,in_out,pay,read_gio)
        VALUES (%d, '%s', '%s',%d,%d,%d);",
        $number,
        $name,
        $ip,
        $in_out,
        $pay,
        $read_gio
    );
    return $query;
}

function camUpdate($query)
{
    $old_ip = '';
    $new_ip = '';
    $name = '';
    $number = '';
    $in_out = '';
    $pay = '';
    $read_gio = '';
    if (!empty($_GET['old_ip'])) {
        $old_ip = $_GET['old_ip'];
    }
    if (!empty($_GET['new_ip'])) {
        $new_ip = $_GET['new_ip'];
    }
    if (!empty($_GET['name'])) {
        $name = $_GET['name'];
    }
    if (!empty($_GET['in_out'])) {
        $in_out = $_GET['in_out'];
    }
    if (!empty($_GET['pay'])) {
        $pay = $_GET['pay'];
    }
    if (!empty($_GET['read_gio'])) {
        $read_gio = $_GET['read_gio'];
    }
    if (!empty($_GET['number'])) {
        $number = $_GET['number'];
    }
    $query = sprintf(
        "UPDATE `ip_cam` SET `number` = '%d', ip='%s', `name` = '%s', `in_out` = '%d', `pay` = '%d', `read_gio`='%d' WHERE `ip` = '%s'",
        $number,
        $new_ip,
        $name,
        $in_out,
        $pay,
        $read_gio,
        $old_ip
    );
    return $query;
}
function camUpdateOpen($query)
{
    $query = sprintf(
        "UPDATE `ip_cam` SET  `open`='%d' WHERE `ip` = '%s'",
        $_GET['open'],
        $_GET['ip']
    );
    return $query;
}
function holidaySingleSearch($query)
{
    $date = '';
    if (!empty($_GET['date'])) {
        $date = $_GET['date'];
    }
    $query = sprintf(
        "SELECT * FROM holiday WHERE date='%d'",
        $date
    );

    return $query;
}

function holidayDelete($query)
{
    $date = '';
    if (!empty($_GET['date'])) {
        $date = $_GET['date'];
    } else {
        return '';
    }
    $query = sprintf(
        "DELETE FROM holiday WHERE date='%s'",
        $date
    );
    return $query;
}
function holidayAdd($query)
{
    $number = '';
    $date = '';
    $weekday = '';
    $description = '';
    $update_date = '';
    $account = '';
    if (!empty($_GET['number'])) {
        $number = $_GET['number'];
    }
    if (!empty($_GET['date'])) {
        $date = $_GET['date'];
    }
    if (!empty($_GET['weekday'])) {
        $weekday = $_GET['weekday'];
    }
    if (!empty($_GET['description'])) {
        $description = $_GET['description'];
    }
    if (!empty($_GET['update_date'])) {
        $update_date = $_GET['update_date'];
    }
    if (!empty($_GET['account'])) {
        $account = $_GET['account'];
    }
    $query = sprintf(
        "INSERT INTO `holiday` (`date`, `weekday`, `description`, `update_date`, `account`, `number`) VALUES ('%s', '%d','%s','%s','%s','%d')",
        $date,
        $weekday,
        $description,
        $update_date,
        $account,
        $number
    );
    return $query;
}

function holidayUpdate($query)
{
    $number = '';
    $old_date = '';
    $new_date = '';
    $weekday = '';
    $description = '';
    $update_date = '';
    $account = '';
    if (!empty($_GET['number'])) {
        $number = $_GET['number'];
    }
    if (!empty($_GET['old_date'])) {
        $old_date = $_GET['old_date'];
    }
    if (!empty($_GET['new_date'])) {
        $new_date = $_GET['new_date'];
    }
    if (!empty($_GET['weekday'])) {
        $weekday = $_GET['weekday'];
    }
    if (!empty($_GET['description'])) {
        $description = $_GET['description'];
    }
    if (!empty($_GET['update_date'])) {
        $update_date = $_GET['update_date'];
    }
    if (!empty($_GET['account'])) {
        $account = $_GET['account'];
    }
    $query = sprintf(
        "UPDATE `holiday` SET `date` = '%s', `weekday` = '%d', `description` = '%s', `update_date` = '%s', `account` = '%s', `number` = '%d' WHERE `holiday`.`date` = '%s'",
        $new_date,
        $weekday,
        $description,
        $update_date,
        $account,
        $number,
        $old_date
    );
    return $query;
}
function dayHolidayUpdate($query)
{
    $query = sprintf(
        "UPDATE `day_holiday` SET `sunday` = '%d', `monday` = '%d', `tuesday` = '%d', `wednesday` = '%d', `thursday` = '%d', `friday` = '%d', `saturday` = '%d' WHERE `id` = '1'",
        $_GET['sunday'],
        $_GET['monday'],
        $_GET['tuesday'],
        $_GET['wednesday'],
        $_GET['thursday'],
        $_GET['friday'],
        $_GET['saturday']
    );
    return $query;
}
function ecpaySingleSearch($query)
{
    $query = sprintf(
        "SELECT * FROM ecpay WHERE id='1'"
    );

    return $query;
}

function ecpayAdd($query)
{   
    $print_status = 0;
    $plus_car_number = 0;
    $merchant_id = '';
    $company_id = '';
    $hash_key = '';
    $hash_iv = '';
    if (!empty($_GET['print_status'])) {
        $print_status = $_GET['print_status'];
    }
    if (!empty($_GET['plus_car_number'])) {
        $plus_car_number = $_GET['plus_car_number'];
    }
    if (!empty($_GET['merchant_id'])) {
        $merchant_id = $_GET['merchant_id'];
    }
    if (!empty($_GET['company_id'])) {
        $company_id = $_GET['company_id'];
    }
    if (!empty($_GET['hash_key'])) {
        $hash_key = $_GET['hash_key'];
    }
    if (!empty($_GET['hash_iv'])) {
        $hash_iv = $_GET['hash_iv'];
    }

    $query = sprintf(
        "INSERT INTO `ecpay` (`id`, `print_status`, `plus_car_number`, `merchant_id`, `company_id`, `hash_key`, `hash_iv`) VALUES (NULL, '%d', '%d', '%s', '%s', '%s', '%s')",
        $print_status,
        $plus_car_number,
        $merchant_id,
        $company_id,
        $hash_key,
        $hash_iv
    );

    return $query;
}

function ecpayUpdate($query)
{
    $print_status = 0;
    $plus_car_number = 0;
    $merchant_id = '';
    $company_id = '';
    $hash_key = '';
    $hash_iv = '';
    $machine_id = '';
    if (!empty($_GET['print_status'])) {
        $print_status = $_GET['print_status'];
    }
    if (!empty($_GET['plus_car_number'])) {
        $plus_car_number = $_GET['plus_car_number'];
    }
    if (!empty($_GET['merchant_id'])) {
        $merchant_id = $_GET['merchant_id'];
    }
    if (!empty($_GET['company_id'])) {
        $company_id = $_GET['company_id'];
    }
    if (!empty($_GET['hash_key'])) {
        $hash_key = $_GET['hash_key'];
    }
    if (!empty($_GET['hash_iv'])) {
        $hash_iv = $_GET['hash_iv'];
    }
    if (!empty($_GET['machine_id'])) {
        $machine_id = $_GET['machine_id'];
    }
    $query = sprintf(
        "UPDATE `ecpay` SET `print_status` = '%d', `plus_car_number` = '%d', `merchant_id` = '%s', `company_id` = '%s', `hash_key` = '%s', `hash_iv` = '%s', `machine_id` = '%s' WHERE `ecpay`.`id` = 1",
        $print_status,
        $plus_car_number,
        $merchant_id,
        $company_id,
        $hash_key,
        $hash_iv,
        $machine_id
    );

    return $query;
}
function historyDateSearch($query)
{
    $start = '';
    $end = '';
    if (!empty($_GET['start'])) {
        $start = $_GET['start'];
    }
    if (!empty($_GET['end'])) {
        $end = $_GET['end'];
    }

    $query = sprintf(
        "SELECT * FROM history
        WHERE time_in BETWEEN '%s' AND '%s';",
        $start,
        $end
    );

    return $query;
}
function historyDelete($query){
    $id = '';
    if (!empty($_GET['id'])) {
        $id = $_GET['id'];
    }

    $query = sprintf(
        "DELETE FROM history WHERE id='%d'",
        $id
    );

    return $query;
}
function historyAdd($query){
    $query = sprintf(
        "INSERT INTO history (car_number,time_in,time_out,time_pay,cost,bill_number,payment,artificial,type,color)
        VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s');",
        $_GET['car_number'],
        $_GET['time_in'],
        $_GET['time_out'],
        $_GET['time_pay'],
        $_GET['cost'],
        $_GET['bill_number'],
        $_GET['payment'],
        $_GET['artificial'],
        $_GET['type'],
        $_GET['color']
    );

    return $query;
}
function payDateSearch($query)
{
    $query = "SELECT * FROM pay_history";
    $start = '';
    $end = '';
    $car_number ='';
    $payment ='';
    if (!empty($_POST['start']) && !empty($_POST['end'])) {
        $start = $_POST['start'];
        $end = $_POST['end'];
        $query .= sprintf( " WHERE time_pay BETWEEN '%s' AND '%s'",$start,$end);
    }
    if (!empty($_POST['car_number'])) {
        $car_number = $_POST['car_number'];
        if(empty($start)){
            $query .= sprintf(" WHERE car_number = '%s'", $car_number);
        }else{
            $query .= sprintf(" AND car_number = '%s'", $car_number);
        }
        
    }
    if (!empty($_POST['payment'])) {
        $payment = $_POST['payment'];
        if(empty($start) && empty($car_number)){
            $query .= sprintf(" WHERE payment = '%s'", $payment);
        }else{
            $query .= sprintf(" AND payment = '%s'", $payment);
        }
    }

    return $query;
}
function payHistoryAdd($query)
{
    $query = sprintf(
        "INSERT INTO pay_history (car_number,time_in,time_pay,cost,bill_number,payment)
        VALUES ('%s', '%s', '%s','%d','%s','%s');",
        $_POST['car_number'],
        $_POST['time_in'],
        $_POST['time_pay'],
        $_POST['cost'],
        $_POST['bill_number'],
        $_POST['payment']
    );
    return $query;
}
function carInsideWithCarNumber($query)
{
    $query = sprintf( "SELECT * FROM cars_inside WHERE car_number = '%s'",$_GET['car_number']);
    return $query;
}
function carInsideWithNumber($query)
{//sprintf( "SELECT * FROM cars_inside WHERE car_number Like '%%s%'", $_GET['number']);
    $query = "SELECT * FROM cars_inside WHERE car_number Like '%".$_GET['number']."%'";
    return $query;
}
function carInsideDateSearch($query)
{
    $query = "SELECT * FROM cars_inside";
    $start = '';
    $end = '';
    if (!empty($_GET['start']) && !empty($_GET['end'])) {
        $start = $_GET['start'];
        $end = $_GET['end'];
        $query .= sprintf( " WHERE time_pay BETWEEN '%s' AND '%s'",$start,$end);
    }

    return $query;
}
function carInsideDelete($query)
{
    $query = "";
    $car_number = '';
    if (!empty($_GET['car_number'])) {
        $car_number = $_GET['car_number'];
        $query = sprintf( "DELETE FROM cars_inside WHERE car_number = '%s'",$car_number);
    }

    return $query;
}
function carInsideAdd($query)
{
    $query = sprintf(
        "INSERT INTO cars_inside (car_number,time_in,gate,picture_url,type,color)
        VALUES ('%s', '%s', '%s','%s','%s','%s');",
        $_POST['car_number'],
        $_POST['time_in'],
        $_POST['gate'],
        $_POST['picture_url'],
        $_POST['type'],
        $_POST['color']
    );

    return $query;
}
function carInsideUpdatePay($query)
{
    $query = sprintf(
        "UPDATE `cars_inside` SET `time_pay` = '%s',`cost` = '%d',`discount` = '%d', `bill_number` = '%s', `payment`= '%s'   WHERE `car_number` = '%s'",
        $_POST['time_pay'],
        $_POST['cost'],
        $_POST['discount'],
        $_POST['bill_number'],
        $_POST['payment'],
        $_POST['car_number']
    );

    return $query;
}
function carImage($query)
{
    $path = $_GET['path'];
    $file_contents = file_get_contents($path);
    $image_base64Data = base64_encode($file_contents);
    return $image_base64Data;
}

$func = $_GET['func'];
$query = '';
$output = true;

if (empty($_GET['func'])) {
    echo 'Please enter your function name<br>';
    exit();   // 終止程序
}

if($conn){
	switch ($func) {
        //查詢所有使用者
        case 'user_search':
            $query = "SELECT * FROM `user`;";
            break;
        //查詢使用者
        case 'user_single_search':
            $query = userSingleSearch($query);
            break;
        //刪除使用者
        case 'user_delete':
            $query = userDelete($query);
            $output = false;
            break;
        //修改使用者
        case 'user_update':
            $query = userUpdate($query);
            $output = false;
            break;
        //新增使用者
        case 'user_add':
            $query = userAdd($query);
            break;
        //修改使用者密碼
        case 'user_password_change':
            $query = userPasswordChange($query);
            break;
        //查詢所有CAM
        case 'cam_search':
            $query = "SELECT * FROM `ip_cam`;";
            break;
        //查詢CAM
        case 'cam_single_search':
            $query = camSingleSearch($query);
            break;
        //刪除CAM
        case 'cam_delete':
            $query = camDelete($query);
            $output = false;
            break;
        //修改CAM
        case 'cam_update':
            $query = camUpdate($query);
            $output = false;
            break;
        //修改CAM開啟狀態
        case 'cam_update_open':
            $query = camUpdateOpen($query);
            $output = false;
            break;
        //新增CAM
        case 'cam_add':
            $query = camAdd($query);
            break;
        //查詢ECPAY
        case 'ecpay_search':
            $query = ecpaySingleSearch($query);
            break;
        //修改ECPAY資料
        case 'ecpay_update':
            $query = ecpayUpdate($query);
            $output = false;
            break;
        //新增ECPAY資料
        case 'ecpay_add':
            $query = ecpayAdd($query);
            break;
        //查詢所有假日
        case 'holiday_search':
            $query = "SELECT * FROM `holiday`;";
            break;
        //查詢假日
        case 'holiday_single_search':
            $query = holidaySingleSearch($query);
            break;
        //刪除假日
        case 'holiday_delete':
            $query = holidayDelete($query);
            $output = false;
            break;
        //修改假日
        case 'holiday_update':
            $query = holidayUpdate($query);
            $output = false;
            break;
        //新增假日
        case 'holiday_add':
            $query = holidayAdd($query);
            $output = false;
            break;
        //查詢日假日
        case 'day_holiday_search':
            $query = "SELECT * FROM `day_holiday` WHERE `id` = '1';";
            break;
        //修改日假日
        case 'day_holiday_update':
            $query = dayHolidayUpdate($query);
            $output = false;
            break;
        //查詢所有歷史紀錄
        case 'history_search':
            $query = "SELECT * FROM `history`;";
            break;
        //查詢期間歷史紀錄
        case 'history_date_search':
            $query = historyDateSearch($query);
            break;
        //刪除歷史紀錄
        case 'history_delete':
            $query = historyDelete($query);
            break;
        //修改歷史紀錄
        case 'history_update':
            $query = holidayUpdate($query);
            $output = false;
            break;
        //新增歷史紀錄
        case 'history_add':
            $query = historyAdd($query);
            $output = false;
            break;
        //查詢所有繳費紀錄
        case 'pay_search':
            $query = "SELECT * FROM `pay_history`;";
            break;
        //查詢期間內繳費紀錄
        case 'pay_dates_search':
            $query = payDateSearch($query);
            break;
        //新增繳費紀錄
        case 'pay_dates_add':
            $query = payHistoryAdd($query);
            $output = false;
            break;
        //月票新增
        case 'regular_pass_add':
            # code...
            break;
        //月票修改
        case 'regular_pass_update':
            # code...
            break;
        //月票刪除
        case 'regular_pass_delete':
            # code...
            break;
        //停車位查詢
        case 'slot_search':
            $query = "SELECT * FROM `floor` WHERE id = 1;";
            break;
        //停車位設定
        case 'slot_update':
            $query = slotUpdate($query);
            $output = false;
            break;
        //場內車子數量查詢
        case 'cars_inside_count':
            $query = "SELECT COUNT(*) FROM `cars_inside`;";
            break;
        //場內車子查詢
        case 'cars_inside':
            $query = "SELECT * FROM `cars_inside`;";
            break;
        //車號場內車子查詢
        case 'cars_inside_with_car_number':
            $query = carInsideWithCarNumber($query);
            break;
        //車號場內車子查詢
        case 'cars_inside_with_number':
            $query = carInsideWithNumber($query);
            break;
        //場內期間車子查詢
        case 'cars_inside_dates_inside':
            $query = carInsideDateSearch($query);
            break;
         //場內車子刪除
        case 'cars_inside_delete':
            $query = carInsideDelete($query);
            $output = false;
            break;
        //場內車子新增
        case 'cars_inside_add':
            $query = carInsideAdd($query);
            $output = false;
            break;
        //場內車子付款資料更新
        case 'cars_inside_update':
            $query = carInsideUpdatePay($query);
            $output = false;
            break;
        //基本設置查詢
        case 'company_info_search':
            $query = "SELECT * FROM `company_info` WHERE id = 1;";
            break;
        //基本設置設定
        case 'company_info_update':
            $query = company_info_Update($query);
            $output = false;
            break;
        //停車位查詢
        case 'fee_search':
            $query = "SELECT * FROM `basic_fee` WHERE id = 1;";
            break;
        //停車位設定
        case 'fee_update':
            $query = feeUpdate($query);
            $output = false;
            break;
        //讀取並傳送圖片
        case 'get_car_image':
            $query = carImage($query);
            break;
        //取得列印設定
        case 'print_search':
            $query = "SELECT * FROM `print_setting` WHERE id = 1;";
            break;
        default:
            # code...
            break;
    }
    
    if(!(empty($query))){
        if($func == 'get_car_image'){
            echo $query;
        }else{
            $result = mysqli_query($conn,$query);
            if($output){
                $jsonData = array();
                while ($row = $result->fetch_assoc()) {
                    $jsonData[] = $row;
                }
                echo json_encode($jsonData);
        
                // $row = $result->fetch_assoc();//拿資料
                // echo json_encode($row);
            }else{
                echo '';
            }
        }
        
    }
    else {
        echo "不正確連接資料庫</br>" . mysqli_connect_error();
    }
}
else {
	echo "未連接到資料庫</br>" . mysqli_connect_error();
}



?>