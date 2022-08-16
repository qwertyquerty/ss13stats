/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `ss14stats` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ss14stats`;

CREATE TABLE IF NOT EXISTS `global_stats` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `type` enum('SERVER_COUNT','PLAYER_COUNT') COLLATE utf8_unicode_ci NOT NULL,
  `value` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `timestamp` (`timestamp`),
  KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `servers` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(256) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `first_seen` datetime NOT NULL,
  `last_seen` datetime NOT NULL,
  `title` varchar(1024) COLLATE utf8_unicode_ci NOT NULL,
  `player_count` int unsigned NOT NULL,
  `online` tinyint unsigned NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `first_seen` (`first_seen`),
  KEY `last_seen` (`last_seen`),
  KEY `player_count` (`player_count`),
  KEY `online` (`online`),
  KEY `url` (`address`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `server_stats` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `server_id` int unsigned NOT NULL,
  `player_count` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `timestamp` (`timestamp`),
  KEY `server_id` (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
