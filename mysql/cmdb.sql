USE asset;
CREATE TABLE `cmdb` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `TS` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `IP` BINARY(16) NOT NULL,
  `HOSTNAME` varchar(50),
  `APPDESC` varchar(500),
  `OWNER` varchar(15),
  `OS` varchar(15),
  `ORG` varchar(100),
   PRIMARY KEY (ID)
);
