CREATE DATABASE  IF NOT EXISTS `stock_trading` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `stock_trading`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: stock_trading
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `market_schedule`
--

DROP TABLE IF EXISTS `market_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `market_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `open_time` time DEFAULT NULL,
  `close_time` time DEFAULT NULL,
  `open_days` varchar(100) DEFAULT NULL,
  `holidays` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `market_schedule`
--

LOCK TABLES `market_schedule` WRITE;
/*!40000 ALTER TABLE `market_schedule` DISABLE KEYS */;
INSERT INTO `market_schedule` VALUES (1,'09:30:00','16:00:00','Monday-Friday','2025-01-01,2025-12-25');
/*!40000 ALTER TABLE `market_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stocks`
--

DROP TABLE IF EXISTS `stocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stocks` (
  `stock_id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `volume` int DEFAULT '1000',
  `opening_price` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`stock_id`),
  UNIQUE KEY `symbol` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stocks`
--

LOCK TABLES `stocks` WRITE;
/*!40000 ALTER TABLE `stocks` DISABLE KEYS */;
INSERT INTO `stocks` VALUES (1,'AAPL','Apple Inc.',164.09,4996,150.00),(2,'GOOGL','Alphabet Inc.',3135.29,2999,2800.00),(3,'TSLA','Tesla Inc.',895.86,4000,700.00),(4,'AMZN','Amazon.com Inc.',3919.08,2500,3400.00),(5,'MSFT','Microsoft Corp.',337.24,6000,295.00),(6,'ASU','Arizona State',1000.00,499,1000.00),(7,'ASUST','Arizona State',500.00,500,500.00),(8,'AZ','Arizona State',1000.00,1000,1000.00);
/*!40000 ALTER TABLE `stocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `stock_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price_at_time` decimal(10,2) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`),
  KEY `user_id` (`user_id`),
  KEY `stock_id` (`stock_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1,4,1,3919.08,'2025-04-26 13:34:39'),(2,1,4,1,3919.08,'2025-04-26 13:39:47'),(3,1,4,-1,3919.08,'2025-04-26 13:45:42'),(4,1,1,1,164.09,'2025-04-26 16:12:22'),(5,1,1,1,164.09,'2025-04-26 16:17:22'),(6,1,1,1,164.09,'2025-04-26 16:17:30'),(7,1,1,1,164.09,'2025-04-26 16:18:15'),(8,1,5,1,337.24,'2025-04-26 16:23:44'),(9,1,5,-1,337.24,'2025-04-26 16:23:53'),(10,1,4,-1,3919.08,'2025-04-26 16:29:55'),(11,1,2,1,3135.29,'2025-04-26 16:30:01'),(12,1,3,1,895.86,'2025-04-26 16:32:33'),(13,1,3,-1,895.86,'2025-04-26 16:32:55'),(14,1,6,1,1000.00,'2025-04-26 18:32:32');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `balance` decimal(10,2) DEFAULT '1000.00',
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `cash_balance` decimal(10,2) DEFAULT '10000.00',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'coreys','Password123',1000.00,'Corey Saunders','coreysaunders.private@gmail.com',2208.35),(2,'mkelly44','Password0',1000.00,'Mark kelly','mkelly44@gmail.com',10000.00),(3,'test01','Password1',1000.00,'Test ASU','test01@gmail.com',10000.00),(4,'test02','Password0',1000.00,'Test ASUST','test02@gmail.com',10000.00),(5,'test03','Password0',1000.00,'Test account','test03@gmail.com',10000.00),(6,'jsmith','Password',1000.00,'Jacob Smith','jsmith@gmail.com',10000.00);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-05 13:50:43
