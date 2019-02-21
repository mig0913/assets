USE  asset;

CREATE TABLE `splunk` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `IP` varchar(15) NOT NULL,
  `HOSTNAME` varchar(50),
   PRIMARY KEY (ID)
);

CREATE TABLE `cmdb` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `TS` TIMESTAMP,
  `DT` varchar(15) NOT NULL,
  `IP` varchar(15) NOT NULL,
  `HOSTNAME` varchar(50),
  `APPDESC` varchar(500),
  `OWNER` varchar(15),
  `OS` varchar(15),
  `ORG` varchar(100),
   PRIMARY KEY (ID)
);
