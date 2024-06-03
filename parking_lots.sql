-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1:3306
-- 產生時間： 2024-06-03 05:30:48
-- 伺服器版本： 8.2.0
-- PHP 版本： 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `test1`
--

-- --------------------------------------------------------

--
-- 資料表結構 `basic_fee`
--

DROP TABLE IF EXISTS `basic_fee`;
CREATE TABLE IF NOT EXISTS `basic_fee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `enter_time_not_count` int NOT NULL DEFAULT '0',
  `before_one_hour_count` tinyint(1) NOT NULL DEFAULT '0',
  `after_one_hour_unit` tinyint(1) NOT NULL DEFAULT '0',
  `weekday_fee` int NOT NULL DEFAULT '0',
  `weekday_most_fee` int NOT NULL DEFAULT '0',
  `holiday_fee` int NOT NULL DEFAULT '0',
  `holiday_most_fee` int NOT NULL DEFAULT '0',
  `weekday_holiday_cross` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `basic_fee`
--

INSERT INTO `basic_fee` (`id`, `enter_time_not_count`, `before_one_hour_count`, `after_one_hour_unit`, `weekday_fee`, `weekday_most_fee`, `holiday_fee`, `holiday_most_fee`, `weekday_holiday_cross`) VALUES
(1, 30, 1, 0, 30, 300, 40, 400, 1);

-- --------------------------------------------------------

--
-- 資料表結構 `cars_inside`
--

DROP TABLE IF EXISTS `cars_inside`;
CREATE TABLE IF NOT EXISTS `cars_inside` (
  `car_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time_in` datetime NOT NULL,
  `time_pay_count` datetime DEFAULT NULL,
  `time_pay` datetime DEFAULT NULL,
  `cost` int DEFAULT NULL,
  `discount` int DEFAULT '0',
  `gate` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bill_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `artificial` tinyint(1) NOT NULL DEFAULT '0',
  `picture_url` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  UNIQUE KEY `car_number` (`car_number`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `company_info`
--

DROP TABLE IF EXISTS `company_info`;
CREATE TABLE IF NOT EXISTS `company_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lot_name` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `company_name` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `company_address` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `company_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `server_token` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cht_chat_id` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `standby_path` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `standby_sec` int DEFAULT '0',
  `auto_upload_server` tinyint(1) NOT NULL DEFAULT '0',
  `standby_play` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `company_info`
--

INSERT INTO `company_info` (`id`, `lot_name`, `company_name`, `company_address`, `company_phone`, `server_token`, `cht_chat_id`, `standby_path`, `standby_sec`, `auto_upload_server`, `standby_play`) VALUES
(1, '鳳山保華', '北將科技', '台中市', '1', '2', '3', '4', 5, 1, 1);

-- --------------------------------------------------------

--
-- 資料表結構 `coupon_history`
--

DROP TABLE IF EXISTS `coupon_history`;
CREATE TABLE IF NOT EXISTS `coupon_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` int NOT NULL,
  `count` int NOT NULL,
  `deadline` datetime NOT NULL,
  `user` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mark` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `coupon_list`
--

DROP TABLE IF EXISTS `coupon_list`;
CREATE TABLE IF NOT EXISTS `coupon_list` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `used` tinyint(1) NOT NULL DEFAULT '0',
  `deadline` datetime NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `day_holiday`
--

DROP TABLE IF EXISTS `day_holiday`;
CREATE TABLE IF NOT EXISTS `day_holiday` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sunday` tinyint(1) NOT NULL DEFAULT '1',
  `monday` tinyint(1) NOT NULL DEFAULT '0',
  `tuesday` tinyint(1) NOT NULL DEFAULT '0',
  `wednesday` tinyint(1) NOT NULL DEFAULT '0',
  `thursday` tinyint(1) NOT NULL DEFAULT '0',
  `friday` tinyint(1) NOT NULL DEFAULT '0',
  `saturday` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `day_holiday`
--

INSERT INTO `day_holiday` (`id`, `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`) VALUES
(1, 1, 0, 0, 0, 0, 0, 1);

-- --------------------------------------------------------

--
-- 資料表結構 `ecpay`
--

DROP TABLE IF EXISTS `ecpay`;
CREATE TABLE IF NOT EXISTS `ecpay` (
  `id` int NOT NULL AUTO_INCREMENT,
  `print_status` int NOT NULL,
  `plus_car_number` tinyint(1) NOT NULL,
  `machine_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1',
  `merchant_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hash_key` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hash_iv` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `ecpay`
--

INSERT INTO `ecpay` (`id`, `print_status`, `plus_car_number`, `machine_id`, `merchant_id`, `company_id`, `hash_key`, `hash_iv`) VALUES
(1, 2, 1, 'SM01', '3085340', '1', 'HwiqPsywG1hLQNuN', 'YqITWD4TyKacYXpn');

-- --------------------------------------------------------

--
-- 資料表結構 `floor`
--

DROP TABLE IF EXISTS `floor`;
CREATE TABLE IF NOT EXISTS `floor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `car_slot` int NOT NULL DEFAULT '0',
  `pregnant_slot` int NOT NULL DEFAULT '0',
  `disabled_slot` int NOT NULL DEFAULT '0',
  `charging_slot` int NOT NULL DEFAULT '0',
  `reserved_slot` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `floor`
--

INSERT INTO `floor` (`id`, `car_slot`, `pregnant_slot`, `disabled_slot`, `charging_slot`, `reserved_slot`) VALUES
(1, 100, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- 資料表結構 `history`
--

DROP TABLE IF EXISTS `history`;
CREATE TABLE IF NOT EXISTS `history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `car_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime NOT NULL,
  `time_pay` datetime DEFAULT NULL,
  `cost` int DEFAULT NULL,
  `bill_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment` char(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `artificial` tinyint(1) NOT NULL DEFAULT '0',
  `type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `holiday`
--

DROP TABLE IF EXISTS `holiday`;
CREATE TABLE IF NOT EXISTS `holiday` (
  `date` date NOT NULL,
  `weekday` int NOT NULL,
  `description` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_date` date DEFAULT NULL,
  `account` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `number` int NOT NULL,
  UNIQUE KEY `date` (`date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `holiday`
--

INSERT INTO `holiday` (`date`, `weekday`, `description`, `update_date`, `account`, `number`) VALUES
('2024-02-29', 5, '228', '2024-04-29', 'parkjohn', 2);

-- --------------------------------------------------------

--
-- 資料表結構 `ip_cam`
--

DROP TABLE IF EXISTS `ip_cam`;
CREATE TABLE IF NOT EXISTS `ip_cam` (
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `in_out` tinyint(1) NOT NULL DEFAULT '0',
  `pay` tinyint(1) NOT NULL DEFAULT '0',
  `open` tinyint(1) NOT NULL DEFAULT '0',
  `number` int NOT NULL DEFAULT '0',
  UNIQUE KEY `ip` (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `ip_cam`
--

INSERT INTO `ip_cam` (`name`, `ip`, `in_out`, `pay`, `open`, `number`) VALUES
('t1', '192.168.1.100', 0, 1, 0, 0),
('t2', '192.168.1.110', 1, 1, 0, 0);

-- --------------------------------------------------------

--
-- 資料表結構 `pay_history`
--

DROP TABLE IF EXISTS `pay_history`;
CREATE TABLE IF NOT EXISTS `pay_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `car_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `time_in` datetime DEFAULT NULL,
  `time_pay` datetime DEFAULT NULL,
  `cost` int DEFAULT NULL,
  `bill_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `regular_pass`
--

DROP TABLE IF EXISTS `regular_pass`;
CREATE TABLE IF NOT EXISTS `regular_pass` (
  `id` int NOT NULL AUTO_INCREMENT,
  `car_number` int NOT NULL,
  `customer_name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` date NOT NULL,
  `due_date` date NOT NULL,
  `cost` int NOT NULL DEFAULT '0',
  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `account` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  UNIQUE KEY `account` (`account`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `user`
--

INSERT INTO `user` (`account`, `password`, `name`, `phone`, `permission`) VALUES
('parkjohn', '123456', 'John', '09123456789', 'A');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
