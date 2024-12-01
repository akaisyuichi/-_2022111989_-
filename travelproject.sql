-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: travelproject
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activities`
--

DROP TABLE IF EXISTS `activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activities` (
  `ActivityID` int NOT NULL AUTO_INCREMENT,
  `TripID` int NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Type` enum('restaurant','attraction') NOT NULL,
  `VisitDate` date NOT NULL,
  `StartTime` time NOT NULL,
  `EndTime` time NOT NULL,
  `RestaurantID` int DEFAULT NULL,
  PRIMARY KEY (`ActivityID`),
  KEY `idx_trip_id` (`TripID`),
  KEY `FK_RestaurantID` (`RestaurantID`),
  CONSTRAINT `FK_RestaurantID` FOREIGN KEY (`RestaurantID`) REFERENCES `restaurants` (`RestaurantID`),
  CONSTRAINT `fk_trip` FOREIGN KEY (`TripID`) REFERENCES `trips` (`TripID`) ON DELETE CASCADE,
  CONSTRAINT `fk_trip_activity` FOREIGN KEY (`TripID`) REFERENCES `trips` (`TripID`) ON DELETE CASCADE,
  CONSTRAINT `fk_trip_id` FOREIGN KEY (`TripID`) REFERENCES `trips` (`TripID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activities`
--

LOCK TABLES `activities` WRITE;
/*!40000 ALTER TABLE `activities` DISABLE KEYS */;
INSERT INTO `activities` VALUES (19,20,'스시잔마이 (난바)','restaurant','2025-01-01','01:00:00','02:00:00',NULL),(20,20,'epais (우메다)','restaurant','2025-01-02','01:00:00','02:00:00',NULL),(21,20,'미츠키 (도톤보리)','restaurant','2025-01-03','22:00:00','23:00:00',NULL),(22,24,'츠지타 (히고바시)','restaurant','2022-01-01','19:00:00','20:00:00',NULL),(23,24,'해유관 수족관 (카이간도리)','attraction','2022-01-02','11:00:00','12:00:00',NULL),(25,24,'유니버셜스튜디오 (사쿠라지마)','attraction','2022-01-09','11:00:00','12:00:00',NULL),(27,25,'palantir technology japan (시부야)','attraction','2024-12-26','12:30:00','14:00:00',NULL),(28,25,'오타나와노렌','restaurant','2024-12-25','00:41:00','01:41:00',NULL),(29,31,'스시잔마이','restaurant','2026-05-01','13:00:00','14:00:00',NULL),(30,32,'스시잔마이','restaurant','2030-10-10','13:00:00','14:00:00',NULL),(32,36,'epais','restaurant','2025-05-05','13:00:00','14:00:00',NULL),(33,42,'토리톤스시','restaurant','2019-01-01','13:01:00','13:20:00',NULL),(34,25,'스시이치','restaurant','2024-12-27','13:01:00','14:02:00',NULL),(36,44,'부타동메이진','restaurant','2023-06-06','13:01:00','16:04:00',NULL),(37,46,'스시잔마이','restaurant','2015-01-04','13:01:00','16:04:00',NULL),(38,25,'센소지','restaurant','2024-12-26','14:02:00','16:04:00',NULL);
/*!40000 ALTER TABLE `activities` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `validate_activity_date` BEFORE INSERT ON `activities` FOR EACH ROW BEGIN
    DECLARE trip_start DATE;
    DECLARE trip_end DATE;

    SELECT StartDate, EndDate
    INTO trip_start, trip_end
    FROM trips
    WHERE TripID = NEW.TripID;

    IF NEW.VisitDate < trip_start OR NEW.VisitDate > trip_end THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '일정 날짜가 여행 계획의 날짜 범위를 벗어납니다.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `prevent_activity_time_overlap` BEFORE INSERT ON `activities` FOR EACH ROW BEGIN
    IF EXISTS (
        SELECT 1
        FROM activities
        WHERE TripID = NEW.TripID
          AND VisitDate = NEW.VisitDate
          AND (NEW.StartTime BETWEEN StartTime AND EndTime
               OR NEW.EndTime BETWEEN StartTime AND EndTime
               OR StartTime BETWEEN NEW.StartTime AND NEW.EndTime
               OR EndTime BETWEEN NEW.StartTime AND NEW.EndTime)
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '일정 시간이 겹칩니다.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `LogActivitiesInsert` AFTER INSERT ON `activities` FOR EACH ROW INSERT INTO activitylogs (ActivityID, ChangeType, ChangedBy)
VALUES (NEW.ActivityID, 'INSERT', USER()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `LogActivitiesUpdate` AFTER UPDATE ON `activities` FOR EACH ROW INSERT INTO activitylogs (ActivityID, ChangeType, ChangedBy)
VALUES (NEW.ActivityID, 'UPDATE', USER()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `LogActivitiesDelete` AFTER DELETE ON `activities` FOR EACH ROW INSERT INTO activitylogs (ActivityID, ChangeType, ChangedBy)
VALUES (OLD.ActivityID, 'DELETE', USER()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `activitylogs`
--

DROP TABLE IF EXISTS `activitylogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activitylogs` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `ActivityID` int NOT NULL,
  `ChangeType` enum('INSERT','UPDATE','DELETE') NOT NULL,
  `ChangedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `ChangedBy` varchar(255) NOT NULL,
  PRIMARY KEY (`LogID`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activitylogs`
--

LOCK TABLES `activitylogs` WRITE;
/*!40000 ALTER TABLE `activitylogs` DISABLE KEYS */;
INSERT INTO `activitylogs` VALUES (1,4,'DELETE','2024-11-28 16:57:16','root@localhost'),(2,3,'UPDATE','2024-11-28 16:58:51','root@localhost'),(3,5,'INSERT','2024-11-29 13:57:24','root@localhost'),(4,6,'INSERT','2024-11-29 14:19:16','root@localhost'),(5,5,'UPDATE','2024-11-29 14:52:30','root@localhost'),(6,5,'DELETE','2024-11-29 14:56:05','root@localhost'),(7,6,'UPDATE','2024-11-29 14:56:50','root@localhost'),(8,6,'DELETE','2024-11-29 14:57:15','root@localhost'),(9,3,'DELETE','2024-11-29 14:57:46','root@localhost'),(10,7,'INSERT','2024-11-29 14:59:43','root@localhost'),(11,7,'DELETE','2024-11-29 15:09:55','root@localhost'),(12,8,'INSERT','2024-11-29 15:21:15','root@localhost'),(13,9,'INSERT','2024-11-29 15:29:43','root@localhost'),(14,9,'DELETE','2024-11-29 15:34:11','root@localhost'),(15,8,'DELETE','2024-11-29 15:34:59','root@localhost'),(16,10,'INSERT','2024-11-29 15:36:25','root@localhost'),(17,11,'INSERT','2024-11-29 15:39:42','root@localhost'),(18,12,'INSERT','2024-11-29 15:55:23','root@localhost'),(19,12,'DELETE','2024-11-29 16:04:44','root@localhost'),(20,11,'DELETE','2024-11-29 16:04:59','root@localhost'),(21,10,'DELETE','2024-11-29 16:05:15','root@localhost'),(22,13,'INSERT','2024-11-29 16:09:07','root@localhost'),(23,13,'UPDATE','2024-11-29 16:16:33','root@localhost'),(24,13,'UPDATE','2024-11-29 16:20:53','root@localhost'),(25,14,'INSERT','2024-11-29 16:29:50','root@localhost'),(26,15,'INSERT','2024-11-29 16:33:43','root@localhost'),(27,16,'INSERT','2024-11-29 16:39:20','root@localhost'),(28,17,'INSERT','2024-11-29 16:40:45','root@localhost'),(29,18,'INSERT','2024-11-29 16:43:56','root@localhost'),(30,19,'INSERT','2024-11-29 16:47:45','root@localhost'),(31,20,'INSERT','2024-11-29 16:48:18','root@localhost'),(32,14,'UPDATE','2024-11-29 16:49:36','root@localhost'),(33,13,'DELETE','2024-11-29 16:49:51','root@localhost'),(34,14,'DELETE','2024-11-29 16:49:51','root@localhost'),(35,15,'DELETE','2024-11-29 16:49:51','root@localhost'),(36,16,'DELETE','2024-11-29 16:49:51','root@localhost'),(37,17,'DELETE','2024-11-29 16:49:51','root@localhost'),(38,18,'DELETE','2024-11-29 16:49:51','root@localhost'),(39,21,'INSERT','2024-11-30 00:57:00','root@localhost'),(40,22,'INSERT','2024-11-30 01:49:16','root@localhost'),(41,23,'INSERT','2024-11-30 01:49:52','root@localhost'),(42,24,'INSERT','2024-11-30 01:52:10','root@localhost'),(43,25,'INSERT','2024-11-30 02:06:25','root@localhost'),(44,26,'INSERT','2024-11-30 02:08:22','root@localhost'),(45,27,'INSERT','2024-11-30 02:08:53','root@localhost'),(46,28,'INSERT','2024-12-01 05:42:11','root@localhost'),(47,26,'DELETE','2024-12-01 06:28:34','root@localhost'),(48,27,'UPDATE','2024-12-01 06:31:18','root@localhost'),(49,24,'DELETE','2024-12-01 06:41:00','root@localhost'),(50,29,'INSERT','2024-12-01 07:33:22','root@localhost'),(51,30,'INSERT','2024-12-01 07:39:20','root@localhost'),(52,31,'INSERT','2024-12-01 07:39:45','root@localhost'),(53,31,'DELETE','2024-12-01 07:40:26','root@localhost'),(54,32,'INSERT','2024-12-01 07:56:37','root@localhost'),(55,33,'INSERT','2024-12-01 08:31:25','root@localhost'),(56,34,'INSERT','2024-12-01 08:45:57','root@localhost'),(57,35,'INSERT','2024-12-01 08:47:50','root@localhost'),(58,36,'INSERT','2024-12-01 08:51:19','root@localhost'),(59,37,'INSERT','2024-12-01 09:47:26','root@localhost'),(60,35,'UPDATE','2024-12-01 10:10:07','root@localhost'),(61,35,'DELETE','2024-12-01 10:10:29','root@localhost'),(62,38,'INSERT','2024-12-01 10:40:53','root@localhost');
/*!40000 ALTER TABLE `activitylogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attractions`
--

DROP TABLE IF EXISTS `attractions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attractions` (
  `AttractionID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Address` varchar(300) NOT NULL,
  `DetailedArea` varchar(100) DEFAULT NULL,
  `Destination` varchar(100) DEFAULT NULL,
  `Rating` decimal(3,2) DEFAULT NULL,
  PRIMARY KEY (`AttractionID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attractions`
--

LOCK TABLES `attractions` WRITE;
/*!40000 ALTER TABLE `attractions` DISABLE KEYS */;
/*!40000 ALTER TABLE `attractions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurants`
--

DROP TABLE IF EXISTS `restaurants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurants` (
  `RestaurantID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Category` varchar(100) DEFAULT NULL,
  `Address` varchar(100) NOT NULL,
  `DetailedArea` varchar(100) DEFAULT NULL,
  `Destination` varchar(100) DEFAULT NULL,
  `Rating` decimal(5,2) DEFAULT NULL,
  `restaurantscol` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`RestaurantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurants`
--

LOCK TABLES `restaurants` WRITE;
/*!40000 ALTER TABLE `restaurants` DISABLE KEYS */;
/*!40000 ALTER TABLE `restaurants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `triplogs`
--

DROP TABLE IF EXISTS `triplogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `triplogs` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `TripID` int NOT NULL,
  `ChangeType` enum('INSERT','UPDATE','DELETE') NOT NULL,
  `ChangedAt` datetime DEFAULT CURRENT_TIMESTAMP,
  `ChangedBy` varchar(255) NOT NULL,
  PRIMARY KEY (`LogID`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `triplogs`
--

LOCK TABLES `triplogs` WRITE;
/*!40000 ALTER TABLE `triplogs` DISABLE KEYS */;
INSERT INTO `triplogs` VALUES (1,4,'DELETE','2024-11-29 14:57:15','root@localhost'),(2,7,'DELETE','2024-11-29 14:57:46','root@localhost'),(3,2,'DELETE','2024-11-29 14:58:22','root@localhost'),(4,8,'INSERT','2024-11-29 14:59:11','root@localhost'),(5,9,'INSERT','2024-11-29 15:20:22','root@localhost'),(6,10,'INSERT','2024-11-29 15:29:11','root@localhost'),(7,9,'DELETE','2024-11-29 15:34:59','root@localhost'),(8,11,'INSERT','2024-11-29 15:35:56','root@localhost'),(9,12,'INSERT','2024-11-29 15:39:28','root@localhost'),(10,13,'INSERT','2024-11-29 15:48:57','root@localhost'),(11,13,'DELETE','2024-11-29 15:52:09','root@localhost'),(12,14,'INSERT','2024-11-29 15:52:39','root@localhost'),(13,15,'INSERT','2024-11-29 15:54:57','root@localhost'),(14,15,'DELETE','2024-11-29 16:04:44','root@localhost'),(15,14,'DELETE','2024-11-29 16:04:51','root@localhost'),(16,12,'DELETE','2024-11-29 16:04:59','root@localhost'),(17,11,'DELETE','2024-11-29 16:05:15','root@localhost'),(18,16,'INSERT','2024-11-29 16:05:34','root@localhost'),(19,16,'DELETE','2024-11-29 16:08:24','root@localhost'),(20,17,'INSERT','2024-11-29 16:08:43','root@localhost'),(21,18,'INSERT','2024-11-29 16:41:16','root@localhost'),(22,19,'INSERT','2024-11-29 16:44:29','root@localhost'),(23,19,'DELETE','2024-11-29 16:46:54','root@localhost'),(24,18,'DELETE','2024-11-29 16:47:04','root@localhost'),(25,20,'INSERT','2024-11-29 16:47:25','root@localhost'),(26,17,'DELETE','2024-11-29 16:49:51','root@localhost'),(28,3,'DELETE','2024-11-30 01:31:01','root@localhost'),(29,21,'INSERT','2024-11-30 01:37:05','root@localhost'),(30,22,'INSERT','2024-11-30 01:44:08','root@localhost'),(31,22,'DELETE','2024-11-30 01:45:38','root@localhost'),(32,23,'INSERT','2024-11-30 01:45:58','root@localhost'),(33,23,'DELETE','2024-11-30 01:48:12','root@localhost'),(34,24,'INSERT','2024-11-30 01:48:53','root@localhost'),(35,25,'INSERT','2024-11-30 02:06:49','root@localhost'),(36,26,'INSERT','2024-12-01 02:32:30','root@localhost'),(37,21,'DELETE','2024-12-01 06:41:00','root@localhost'),(38,27,'INSERT','2024-12-01 07:05:44','root@localhost'),(39,28,'INSERT','2024-12-01 07:19:39','root@localhost'),(40,29,'INSERT','2024-12-01 07:24:01','root@localhost'),(41,30,'INSERT','2024-12-01 07:28:32','root@localhost'),(42,30,'DELETE','2024-12-01 07:32:17','root@localhost'),(43,29,'DELETE','2024-12-01 07:32:22','root@localhost'),(44,31,'INSERT','2024-12-01 07:32:48','root@localhost'),(45,32,'INSERT','2024-12-01 07:38:45','root@localhost'),(46,33,'INSERT','2024-12-01 07:42:12','root@localhost'),(47,34,'INSERT','2024-12-01 07:43:41','root@localhost'),(48,35,'INSERT','2024-12-01 07:53:21','root@localhost'),(49,35,'DELETE','2024-12-01 07:55:17','root@localhost'),(50,34,'DELETE','2024-12-01 07:55:22','root@localhost'),(51,33,'DELETE','2024-12-01 07:55:29','root@localhost'),(52,36,'INSERT','2024-12-01 07:56:08','root@localhost'),(53,37,'INSERT','2024-12-01 08:03:21','root@localhost'),(54,38,'INSERT','2024-12-01 08:14:43','root@localhost'),(55,39,'INSERT','2024-12-01 08:26:30','root@localhost'),(56,40,'INSERT','2024-12-01 08:29:22','root@localhost'),(57,41,'INSERT','2024-12-01 08:30:24','root@localhost'),(58,41,'DELETE','2024-12-01 08:30:41','root@localhost'),(59,42,'INSERT','2024-12-01 08:31:01','root@localhost'),(60,43,'INSERT','2024-12-01 08:39:29','root@localhost'),(61,44,'INSERT','2024-12-01 08:50:30','root@localhost'),(62,45,'INSERT','2024-12-01 08:55:24','root@localhost'),(63,46,'INSERT','2024-12-01 09:47:04','root@localhost'),(64,47,'INSERT','2024-12-01 10:38:38','root@localhost'),(65,48,'INSERT','2024-12-01 10:45:31','root@localhost');
/*!40000 ALTER TABLE `triplogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trips` (
  `TripID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `TripName` varchar(100) NOT NULL,
  `Destination` varchar(100) NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  PRIMARY KEY (`TripID`),
  KEY `idx_user_id` (`UserID`),
  CONSTRAINT `fk_user_trip` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  CONSTRAINT `FK_UserID` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trips`
--

LOCK TABLES `trips` WRITE;
/*!40000 ALTER TABLE `trips` DISABLE KEYS */;
INSERT INTO `trips` VALUES (1,5,'osakaeating','osaka','2024-12-12','2024-12-15'),(5,6,'알콩달콩','오사카','2024-01-01','2024-01-03'),(8,6,'데이트','오사카','2024-01-06','2024-01-10'),(10,6,'먹방2','오사카','2024-02-05','2024-02-09'),(20,6,'먹방1','오사카','2025-01-01','2025-01-04'),(24,6,'링고','오사카','2022-01-01','2022-01-09'),(25,6,'팔란티어방문여행','도쿄','2024-12-25','2024-12-28'),(26,1,'chicken','오사카','2031-02-01','2023-02-02'),(27,6,'바훈우니여행','삿포로','2026-01-01','2026-01-04'),(28,6,'카니여행','삿포로','2026-02-20','2026-02-27'),(31,6,'힘들다','오사카','2026-05-01','2026-05-04'),(32,6,'karpgod','오사카','2030-10-10','2030-10-13'),(36,6,'shanker','오사카','2025-05-05','2025-05-10'),(37,6,'빅데이터닥터','오사카','2025-06-01','2025-06-05'),(38,6,'키키키','오사카','2025-08-08','2025-08-12'),(39,6,'구구구','도쿄','2090-01-01','2090-01-04'),(40,6,'zlzlzl','삿포로','2070-01-01','2070-01-04'),(42,6,'일론머스크','삿포로','2019-01-01','2019-01-04'),(43,6,'피터틸','도쿄','2000-01-01','2000-01-05'),(44,6,'살려줘','삿포로','2023-06-06','2023-06-09'),(45,6,'윤작가','후쿠오카','2027-01-01','2027-01-08'),(46,6,'김승호','오사카','2015-01-01','2015-01-19'),(47,6,'여행2','오사카','2025-05-18','2025-05-22'),(48,6,'배고파','도쿄','2029-04-02','2029-05-01');
/*!40000 ALTER TABLE `trips` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `prevent_trip_date_overlap` BEFORE INSERT ON `trips` FOR EACH ROW BEGIN
    IF EXISTS (
        SELECT 1
        FROM trips
        WHERE (NEW.StartDate BETWEEN StartDate AND EndDate)
           OR (NEW.EndDate BETWEEN StartDate AND EndDate)
           OR (StartDate BETWEEN NEW.StartDate AND NEW.EndDate)
           OR (EndDate BETWEEN NEW.StartDate AND NEW.EndDate)
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '해당 날짜에 이미 여행 계획이 존재합니다.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `LogTripsInsert` AFTER INSERT ON `trips` FOR EACH ROW INSERT INTO triplogs (TripID, ChangeType, ChangedBy)
VALUES (NEW.TripID, 'INSERT', USER()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `LogTripsUpdate` AFTER UPDATE ON `trips` FOR EACH ROW INSERT INTO triplogs (TripID, ChangeType, ChangedBy)
VALUES (NEW.TripID, 'UPDATE', USER()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `LogTripsDelete` AFTER DELETE ON `trips` FOR EACH ROW INSERT INTO triplogs (TripID, ChangeType, ChangedBy)
VALUES (OLD.TripID, 'DELETE', USER()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(150) NOT NULL,
  `Password` varchar(255) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'kim','kk@gmail.com','scrypt:32768:8:1$86oe11DTf95Khk7I$25f25666e66aba2e7c1ade87294338aef661067da85d8db0a76fdb5aa8e7252e7b5d1a6c2462b2225026b9382f0eabf2f9d2a06c4bb19d03ab3aa61cd53fd1df'),(4,'kims','kkk@gmail.com','scrypt:32768:8:1$6rDY0CFpe5dbxcwo$624d02b37f75fcb7ca1fc06f301abeec59025b5daea0b8c140ee076da36ed90f20d27a3969f029ac3004abae302004f7ae3a1bf7b6ac3eb37b5627abcd11d5b9'),(5,'yoons','tqqq@gmail.com','scrypt:32768:8:1$ymGk0G509jKihdL0$c53b6ca4cccec875e1a418a25b31440aeba849750021a5526e6e4520d2f49f19452a4ffbf25a595d7313881a7200b11e29f988b88210ea0891f15ba9a63755a4'),(6,'kim','kim@gmail.com','scrypt:32768:8:1$TUoCkHz7jZ2lgAE9$7a5d393de5d14aa3895401b39848359334d95dd2b84410590e191adf9208b879eacbfe153dc16d8ba656c5fb1679a0b8851670eb00b3faeba841e1f688858f31'),(11,'배유근','bae@gmail.com','scrypt:32768:8:1$wnvg8QcvQzJQdSyy$b959e5735057ffad2a797811d12b6ddf10e948036e77b29569883c4bbcade2a8d8d065b1adb844e467fdaed6e9db73c0dedd221926e9060f85b7f5de1f81cbc6'),(12,'윤서인','yoon@gmail.com','scrypt:32768:8:1$wJAYhtuSXJ8UYLS8$83684293c883012fc5f9ac048fe237bb3be7348a1f921264c414832bc96969c9f41815f21ba034ac699e5905fe1a730ed9f0532df1bb1c70767736dd1c7969aa'),(13,'문도원','moon@gmail.com','scrypt:32768:8:1$0ZZsKyKYTyPZJYlv$4794039230c76d9b4396eb9682e4ee9cb6f03950a1d5476a748e55c9f0203018acdc4784b4ba38f4e335bb8662e2d900b089f1339a21f9c22df0079a893266d2'),(14,'카리나','kar@gmail.com','scrypt:32768:8:1$fgkHr1aqxZGuGEfj$0bea782bb475071f2e62c2da9242279b66e332f0b209bfe5784dbf5b02a5daaad726294a297c6a700a8e141ceb233925418316bd9b4034b61c4f79082f514730'),(15,'lany','lany@gmail.com','scrypt:32768:8:1$AAWybvz0fq3NbB99$03d616406ac137e411523636b02ea16357c24bbfa429235c6b5e5f70f0c43c586ac6bc8778aa90582744818cf5bed29bb7eda2fd97912c3560c889968fa87927');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'travelproject'
--

--
-- Dumping routines for database 'travelproject'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-01 19:01:56
