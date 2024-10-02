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
    
    if (!empty($_GET['pregnant'])) {
        $pregnant = $_GET['pregnant'];
    }
    
    if (!empty($_GET['disabled'])) {
        $disabled = $_GET['disabled'];
    }
    
    if (!empty($_GET['charging'])) {
        $charging = $_GET['charging'];
    }
    
    if (!empty($_GET['reserved'])) {
        $reserved = $_GET['reserved'];
    }
    
    $query = sprintf(
        "UPDATE floor SET car_slot = '%d', pregnant_slot = '%d', disabled_slot = '%d', charging_slot = '%d', reserved_slot = '%d', car_left='%d', pregnant_left='%d', disabled_left='%d', charging_left='%d' WHERE floor.id = 1",
        $car,
        $pregnant,
        $disabled,
        $charging,
        $reserved,
        $_GET['car_left'],
        $_GET['pregnant_left'],
        $_GET['disabled_left'],
        $_GET['charging_left']
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
        "UPDATE company_info SET lot_name = '%s', company_name = '%s', company_address = '%s', company_phone = '%s', server_token = '%s', cht_chat_id = '%s', standby_path = '%s', standby_sec = '%d', auto_upload_server = '%d', standby_play = '%d', parking_id = '%s', parking_area = '%s', parking_address = '%s', parking_apikey = '%s' WHERE company_info.id = 1",
        $_GET['lot_name'],
        $_GET['company_name'],
        $_GET['company_address'],
        $_GET['company_phone'],
        $_GET['server_token'],
        $_GET['cht_chat_id'],
        $_GET['standby_path'],
        $_GET['standby_sec'],
        $_GET['auto_upload_server'],
        $_GET['standby_play'],
        $_GET['parking_id'],
        $_GET['parking_area'],
        $_GET['parking_address'],
        $_GET['parking_apikey']
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
function camUpdateClose($query)
{
    $query = sprintf(
        "UPDATE `ip_cam` SET  `close`='%d' WHERE `ip` = '%s'",
        $_GET['close'],
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
        "UPDATE `ecpay` SET `print_status` = '%d', `plus_car_number` = '%d', `merchant_id` = '%s', `company_id` = '%s', `hash_key` = '%s', `hash_iv` = '%s', `machine_id` = '%s', `test` = '%s' WHERE `ecpay`.`id` = 1",
        $print_status,
        $plus_car_number,
        $merchant_id,
        $company_id,
        $hash_key,
        $hash_iv,
        $machine_id,
        $_GET['test']
    );

    return $query;
}
function historyDateSearch($query)
{
    $start = '';
    $end = '';
    if (!empty($_POST['start'])) {
        $start = $_POST['start'];
    }
    if (!empty($_POST['end'])) {
        $end = $_POST['end'];
    }

    $query = sprintf(
        "SELECT * FROM history
        WHERE time_in BETWEEN '%s' AND '%s'
        ORDER BY UNIX_TIMESTAMP(time_in) DESC;",
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
        "INSERT INTO history (car_number,time_in,time_out,time_pay,cost,bill_number,payment,artificial,type,color,picture_url)
        VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s');",
        $_POST['car_number'],
        $_POST['time_in'],
        $_POST['time_out'],
        $_POST['time_pay'],
        $_POST['cost'],
        $_POST['bill_number'],
        $_POST['payment'],
        $_POST['artificial'],
        $_POST['type'],
        $_POST['color'],
        $_POST['path']
    );

    return $query;
}
function serverHistoryDateSearch($query)
{
    $start = '';
    $end = '';
    if (!empty($_POST['start'])) {
        $start = $_POST['start'];
    }
    if (!empty($_POST['end'])) {
        $end = $_POST['end'];
    }

    $query = sprintf(
        "SELECT * FROM server_history
        WHERE time BETWEEN '%s' AND '%s'
        ORDER BY UNIX_TIMESTAMP(time) DESC;",
        $start,
        $end
    );

    return $query;
}
function serverHistoryDelete($query){
    $id = '';
    if (!empty($_GET['id'])) {
        $id = $_GET['id'];
    }

    $query = sprintf(
        "DELETE FROM server_history WHERE id='%d'",
        $id
    );

    return $query;
}
function serverHistoryDeleteDate($query){
    $date = '';
    if (!empty($_POST['date'])) {
        $date = $_POST['date'];
    }

    $query = sprintf(
        "DELETE FROM server_history
        WHERE time < '%s'",
        $date
    );

    return $query;
}
function serverHistoryAdd($query){
    $query = sprintf(
        "INSERT INTO server_history (time,description)
        VALUES ('%s', '%s');",
        $_POST['time'],
        $_POST['description']
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
    $query .= " ORDER BY UNIX_TIMESTAMP(time_pay) DESC";

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
function payHistoryDeleteDate($query){
    $date = '';
    if (!empty($_POST['date'])) {
        $date = $_POST['date'];
    }

    $query = sprintf(
        "DELETE FROM pay_history
        WHERE time < '%s'",
        $date
    );

    return $query;
}
function carInsideWithCarNumber($query)
{
    $query = sprintf( "SELECT * FROM cars_inside WHERE car_number = '%s'",$_GET['car_number']);
    return $query;
}
function carInsideWithCarNumberAndDate($query)
{
    $query = sprintf( "SELECT * FROM cars_inside 
                        WHERE car_number = '%s'
                        AND time_in BETWEEN '%s' AND '%s'",
                        $_POST['car_number'],
                        $_POST['start'],
                        $_POST['end']);
    return $query;
}
function carInsideWithNumber($query)
{
    $query = "SELECT * FROM cars_inside WHERE car_number Like '%".$_GET['number']."%'";
    return $query;
}
function carInsideDateSearch($query)
{
    $query = "SELECT * FROM cars_inside";
    $start = '';
    $end = '';
    if (!empty($_POST['start']) && !empty($_POST['end'])) {
        $start = $_POST['start'];
        $end = $_POST['end'];
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
        "UPDATE `cars_inside` SET `time_pay` = '%s',`cost` = '%d',`discount` = '%d', `bill_number` = '%s', `payment`= '%s'   WHERE `car_number` = '%s';",
        $_POST['time_pay'],
        $_POST['cost'],
        $_POST['discount'],
        $_POST['bill_number'],
        $_POST['payment'],
        $_POST['car_number']
    );

    return $query;
}
function carInsideDeletePay($query)
{
    $query = sprintf(
        "UPDATE `cars_inside` SET `time_pay` = NULL WHERE `car_number` = '%s';",
        $_GET['car_number']
    );

    return $query;
}
function carInsideUpdatePayWithServerTime($query)
{
    $now = new DateTime(null, new DateTimeZone('Asia/Taipei'));

    $query = sprintf(
        "UPDATE `cars_inside` SET `time_pay` = '%s',`cost` = '%d',`discount` = '%d', `bill_number` = '%s', `payment`= '%s'   WHERE `car_number` = '%s';",
        $now->format('Y-m-d H:i:s'),
        $_POST['cost'],
        $_POST['discount'],
        $_POST['bill_number'],
        $_POST['payment'],
        $_POST['car_number']
    );

    return $query;
}
function carInsideUpdateNumber($query)
{
    $query = sprintf(
        "UPDATE `cars_inside` SET `car_number` = '%s', `time_in`= '%s'   WHERE `car_number` = '%s';",
        $_POST['new_number'],
        $_POST['time_in'],
        $_POST['old_number']
    );

    return $query;
}
function printUpdate($query){
    $query = sprintf(
        "UPDATE `print_setting` SET `new_roll` = '%s', `warning`= '%s',`print_invoice`= '%s',`print_revenue`= '%s',`print_coupon`= '%s'   WHERE `id` = 1;",
        $_GET['new_roll'],
        $_GET['warning'],
        $_GET['print_invoice'],
        $_GET['print_revenue'],
        $_GET['print_coupon']
    );

    return $query;
}

function printPaperLeftUpdate($query){
    $query = sprintf(
        "UPDATE `print_setting` SET `pay_left` = '%s'  WHERE `id` = 1;",
        $_GET['pay_left']);

    return $query;
}

function couponHistoryAdd($query)
{
    $query = sprintf(
        "INSERT INTO coupon_history (time_fee, amount,count,deadline,user,mark)
        VALUES ('%s', '%s', '%s', '%s','%s','%s');",
        $_POST['time_fee'],
        $_POST['amount'],
        $_POST['count'],
        $_POST['deadline'],
        $_POST['user'],
        $_POST['mark']
    );

    return $query;
}
function couponSettingUpdate($query){
    $query = sprintf(
        "UPDATE `coupon_setting` SET `time_fee` = '%s', `amount`= '%s',`paper`= '%s',`deadline`= '%s', `code` = '%s',`print`= '%s'   WHERE `id` = 1;",
        $_POST['time_fee'],
        $_POST['amount'],
        $_POST['paper'],
        $_POST['deadline'],
        $_POST['code'],
        $_POST['print']
    );

    return $query;
}
function couponSettingUpdateStop($query){
    $query = "UPDATE `coupon_setting` SET `print`= '0'   WHERE `id` = 1;";

    return $query;
}
function couponListAdd($query)
{
    $query = sprintf(
        "INSERT INTO coupon_list (id,deadline)
        VALUES ('%s', '%s');",
        $_POST['id'],
        $_POST['deadline']
    );

    return $query;
}
function couponListSearch($query)
{
    $query = sprintf(
        "SELECT * FROM coupon_list WHERE id='%s';",
        $_GET['id']
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
function moneyCountUpdate($query){
    $query = sprintf(
        "UPDATE `money_count` SET `five` = '%s', `ten`= '%s',`fifty`= '%s',`hundred`= '%s'  WHERE `id` = 1;",
        $_GET['five'],
        $_GET['ten'],
        $_GET['fifty'],
        $_GET['hundred']
    );

    return $query;
}
function moneyBasicUpdate($query){
    $query = sprintf(
        "UPDATE `money_basic` SET `five_basic` = '%s', `ten_basic`= '%s',`fifty_basic`= '%s',`five_alert` = '%s', `ten_alert`= '%s',`fifty_alert`= '%s'  WHERE `id` = 1;",
        $_GET['five_basic'],
        $_GET['ten_basic'],
        $_GET['fifty_basic'],
        $_GET['five_alert'],
        $_GET['ten_alert'],
        $_GET['fifty_alert']
    );
    return $query;
}
function moneyRefundUpdate($query){
    $query = sprintf(
        "UPDATE `money_refund` SET `five` = '%s', `ten`= '%s',`fifty`= '%s',`refund` = '1' WHERE `id` = 1;",
        $_GET['five'],
        $_GET['ten'],
        $_GET['fifty']
    );

    return $query;
}
function moneyRefundStop($query){
    $query = sprintf(
        "UPDATE `money_refund` SET `refund` = '0' WHERE `id` = 1;"
    );

    return $query;
}
function moneySupplyUpdate($query){
    $query = sprintf(
        "UPDATE `money_supply` SET `five_count` = '%s', `ten_count`= '%s',`fifty_count`= '%s' WHERE `id` = 1;",
        $_GET['five_count'],
        $_GET['ten_count'],
        $_GET['fifty_count']
    );

    return $query;
}
function moneySupplyStart($query){
    $query = sprintf(
        "UPDATE `money_supply` SET `five` = '%s', `ten`= '%s',`fifty`= '%s',`five_count` = '0', `ten_count`= '0',`fifty_count`= '0',`supply` = '1' WHERE `id` = 1;",
        $_GET['five'],
        $_GET['ten'],
        $_GET['fifty']
    );

    return $query;
}
function regularPassAdd($query)
{
    $query = sprintf(
        "INSERT INTO regular_pass (car_number,customer_name,start_date,due_date,phone_number)
        VALUES ('%s', '%s', '%s','%s','%s');",
        $_GET['car_number'],
        $_GET['customer_name'],
        $_GET['start_date'],
        $_GET['due_date'],
        $_GET['phone_number']
    );
    return $query;
}
function regularPassUpdate($query)
{
    $query = sprintf(
        "UPDATE regular_pass SET `car_number` = '%s' , `customer_name` = '%s' , `start_date`= '%s' , `due_date` = '%s' , `phone_number` = '%s'  WHERE id = %d;",
        $_GET['car_number'],
        $_GET['customer_name'],
        $_GET['start_date'],
        $_GET['due_date'],
        $_GET['phone_number'],
        $_GET['id'],
    );
    return $query;
}
function regularPassDelete($query)
{
    $query = sprintf(
        "DELETE FROM regular_pass WHERE `id` = '%d';",
        $_GET['id']
    );
    return $query;
}
function regularPassSingleSearch($query)
{
    $query = sprintf(
        "SELECT * FROM regular_pass WHERE `car_number` = '%s';",
        $_GET['car_number']
    );
    return $query;
}
function moneySupplyStop($query){
    $query = sprintf(
        "UPDATE `money_supply` SET `supply` = '0' WHERE `id` = 1;"
    );

    return $query;
}
function LinePayUpdate($query){
    $query = sprintf(
        "UPDATE `line_pay` SET `ChannelId` = '%s', `ChannelSecret`= '%s', `test` = '%d' WHERE `id` = 1;",
        $_GET['ChannelId'],
        $_GET['ChannelSecret'],
        $_GET['test']
    );

    return $query;
}
function accountPreferenceSingleSearch($query)
{
    $ip = '';
    $vpn = '';
    if (!empty($_GET['ip'])) {
        $ip = $_GET['ip'];
    }
    if (!empty($_GET['vpn'])) {
        $ip = $_GET['vpn'];
    }
    $query = sprintf(
        "SELECT * FROM account_preference WHERE ip='%s'",
        $ip
    );

    return $query;
}
function accountPreferenceAdd($query)
{
    $ip = '';
    if (!empty($_GET['ip'])) {
        $ip = $_GET['ip'];
    }
    $query = sprintf(
        "INSERT INTO account_preference (ip,vpn)
        VALUES (%s, '%s');",
        $ip,
        $vpn
    );
    return $query;
}
function accountPreferenceDelete($query)
{
    $ip = '';
    if (!empty($_GET['ip'])) {
        $ip = $_GET['ip'];
    }
    $query = sprintf(
        "DELETE FROM account_preference WHERE ip='%s'",
        $ip
    );
    return $query;
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
        //修改CAM關閉狀態
        case 'cam_update_close':
            $query = camUpdateClose($query);
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
            $query = "SELECT * FROM `history` ORDER BY UNIX_TIMESTAMP(time_in) DESC;";
            break;
        //查詢最新二十筆歷史紀錄
        case 'history_search_20':
            $query = "SELECT * FROM `history` ORDER BY UNIX_TIMESTAMP(time_in) DESC LIMIT 20;";
            break;
        //查詢最新二十筆歷史紀錄
        case 'history_search_10':
            $query = "SELECT * FROM `history` ORDER BY UNIX_TIMESTAMP(time_in) DESC LIMIT 10;";
            break;
        //查詢期間歷史紀錄
        case 'history_date_search':
            $query = historyDateSearch($query);
            break;
        //刪除歷史紀錄
        case 'history_delete':
            $query = historyDelete($query);
            $output = false;
            break;
        //新增歷史紀錄
        case 'history_add':
            $query = historyAdd($query);
            $output = false;
            break;
        //查詢所有繳費紀錄
        case 'pay_search':
            $query = "SELECT * FROM `pay_history` ORDER BY UNIX_TIMESTAMP(time_pay) DESC;";
            break;
        //查詢最新二十筆繳費紀錄
        case 'pay_search_20':
            $query = "SELECT * FROM `pay_history` ORDER BY UNIX_TIMESTAMP(time_pay) DESC LIMIT 20;";
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
        //刪除繳費記錄
        case 'pay_dates_delete':
            $query = payHistoryDeleteDate($query);
            $output = false;
            break;
        //月票新增
        case 'regular_pass_add':
            $query = regularPassAdd($query);
            $output = false;
            break;
        //月票修改
        case 'regular_pass_update':
            $query = regularPassUpdate($query);
            $output = false;
            break;
        //月票刪除
        case 'regular_pass_delete':
            $query = regularPassDelete($query);
            $output = false;
            break;
        //月票查詢
        case 'regular_pass_search':
            $query = "SELECT * FROM `regular_pass`;";
            break;
        case 'regular_pass_single_search':
            $query = regularPassSingleSearch($query);
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
        //車號場內車子查詢特定號碼
        case 'cars_inside_with_car_number':
            $query = carInsideWithCarNumber($query);
            break;
        //車號場內車子查詢相關號碼
        case 'cars_inside_with_number':
            $query = carInsideWithNumber($query);
            break;
        //場內期間車子查詢
        case 'cars_inside_dates_inside':
            $query = carInsideDateSearch($query);
            break;
        //車號場內車子查詢相關號碼
        case 'cars_inside_with_number_and_dates':
            $query = carInsideWithCarNumberAndDate($query);
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
        //場內車子付款資料更新
        case 'cars_inside_update_with_server_time':
            $query = carInsideUpdatePayWithServerTime($query);
            $output = false;
            break;
        //場內車子付款資料刪除
        case 'cars_inside_pay_delete':
            $query = carInsideDeletePay($query);
            $output = false;
            break;
        //場內車子付款資料更新
        case 'cars_inside_update_number':
            $query = carInsideUpdateNumber($query);
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
        //列印設定
        case 'print_update':
            $query = printUpdate($query);
            $output = false;
            break;
        case 'print_update_paper_left':
            $query = printPaperLeftUpdate($query);
            $output = false;
            break;
        //取得優惠券歷史
        case 'coupon_history_search':
            $query = "SELECT * FROM `coupon_history`";
            break;
        //新增優惠券歷史
        case 'coupon_history_add':
            $query = couponHistoryAdd($query);
            $output = false;
            break;
        //取得優惠券設定
        case 'coupon_setting_search':
            $query = "SELECT * FROM `coupon_setting` where `id` = 1";
            break;
        //優惠券設定
        case 'coupon_setting_update':
            $query = couponSettingUpdate($query);
            $output = false;
            break;
        //停止列印優惠券
        case 'coupon_setting_update_stop':
            $query = couponSettingUpdateStop($query);
            $output = false;
            break;
        //新增優惠券列表
        case 'coupon_list_add':
            $query = couponListAdd($query);
            $output = false;
            break;
        //查詢優惠券列表成員
        case 'coupon_list_search':
            $query = couponListSearch($query);
            break;
        //查詢優惠券列表
        case 'coupon_list_search_all':
            $query = "SELECT * FROM coupon_list";
            break;
        case 'money_count_search':
            $query = "SELECT * FROM money_count WHERE `id` = '1';";
            break;
        case 'money_count_update':
            $query = moneyCountUpdate($query);
            $output = false;
            break;
        case 'money_basic_search':
            $query = "SELECT * FROM money_basic WHERE `id` = '1';";
            break;
        case 'money_basic_update':
            $query = moneyBasicUpdate($query);
            $output = false;
            break;
        case 'money_refund_search':
            $query = "SELECT * FROM money_refund WHERE `id` = '1';";
            break;
        case 'money_refund_update':
            $query = moneyRefundUpdate($query);
            $output = false;
            break;
        case 'money_refund_stop':
            $query = moneyRefundStop($query);
            $output = false;
            break;
        case 'money_supply_search':
            $query = "SELECT * FROM money_supply WHERE `id` = '1';";
            break;
        case 'money_supply_update':
            $query = moneySupplyUpdate($query);
            $output = false;
            break;
        case 'money_supply_start':
            $query = moneySupplyStart($query);
            $output = false;
            break;
        case 'money_supply_stop':
            $query = moneySupplyStop($query);
            $output = false;
            break;
        case 'get_server_time':
            $now = new DateTime(null, new DateTimeZone('Asia/Taipei'));
            $query = $now->format('Y-m-d H:i:s');
            break;
        case 'line_pay_search':
            $query = "SELECT * FROM line_pay WHERE `id` = '1';";
            break;
        case 'line_pay_update':
            $query = LinePayUpdate($query);
            $output = false;
            break;
        //查詢所有log歷史紀錄
        case 'server_history_search':
            $query = "SELECT * FROM `server_history` ORDER BY UNIX_TIMESTAMP(time) DESC;";
            break;
        //查詢最新二十筆log歷史紀錄
        case 'server_history_search_20':
            $query = "SELECT * FROM `server_history` ORDER BY UNIX_TIMESTAMP(time) DESC LIMIT 20;";
            break;
        //查詢log期間歷史紀錄
        case 'server_history_date_search':
            $query = serverHistoryDateSearch($query);
            break;
        //刪除log紀錄
        case 'server_history_delete':
            $query = serverHistoryDelete($query);
            $output = false;
            break;
        //刪除log某期間紀錄
        case 'server_history_date_delete':
            $query = serverHistoryDeleteDate($query);
            $output = false;
            break;
        //新增log歷史紀錄
        case 'server_history_add':
            $query = serverHistoryAdd($query);
            $output = false;
            break;
        
        case 'account_preference_add':
            $query = accountPreferenceAdd($query);
            $output = false;
            break;
        case 'account_preference_delete':
            $query = accountPreferenceDelete($query);
            $output = false;
            break;
        case 'account_preference_search':
            $query = "SELECT * FROM account_preference;";
            break;
        case 'account_preference_single_search':
            $query = accountPreferenceSingleSearch($query);
            break;
        default:
            # code...
            break;
    }
    
    if(!(empty($query))){
        if($func == 'get_car_image'){
            echo $query;
        }elseif($func == 'get_server_time'){
            echo $query;
        }else{
            $result = mysqli_query($conn,$query);
            if($output){
                $jsonData = array();
                while ($row = $result->fetch_assoc()) {
                    $jsonData[] = $row;
                }
                echo json_encode($jsonData);
        
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