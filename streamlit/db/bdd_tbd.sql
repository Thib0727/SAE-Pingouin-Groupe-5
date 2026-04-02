DROP DATABASE IF EXISTS `exploit`;

CREATE DATABASE IF NOT EXISTS `exploit`;

USE `exploit`;

CREATE TABLE IF NOT EXISTS exploit.tblfinstep LIKE mes4.tblfinstep;
CREATE TABLE IF NOT EXISTS exploit.tblbufferpos LIKE mes4.tblbufferpos;
CREATE TABLE IF NOT EXISTS exploit.tblbuffer LIKE mes4.tblbuffer;
CREATE TABLE IF NOT EXISTS exploit.tblpartsreport LIKE mes4.tblpartsreport;
CREATE TABLE IF NOT EXISTS exploit.tblmainterror LIKE mes4.tblmainterror;
CREATE TABLE IF NOT EXISTS exploit.tblpalletpos LIKE mes4.tblpalletpos;
CREATE TABLE IF NOT EXISTS exploit.tblmachinereport LIKE mes4.tblmachinereport;
CREATE TABLE IF NOT EXISTS exploit.tblbufferpos LIKE mes4.tblbufferpos;
CREATE TABLE IF NOT EXISTS exploit.tblparts LIKE mes4.tblparts;
CREATE TABLE IF NOT EXISTS exploit.tblorderpos LIKE mes4.tblorderpos;
CREATE TABLE IF NOT EXISTS exploit.tblorder LIKE mes4.tblorder;

ALTER TABLE tblbufferpos 
ADD CONSTRAINT fk_bufferpos 
FOREIGN KEY (PNo) REFERENCES tblparts(PNo);

-- 1. Tables de base (Niveau 1)
INSERT INTO exploit.tblparts SELECT * FROM mes4.tblparts;
INSERT INTO exploit.tblorder SELECT * FROM mes4.tblorder;
INSERT INTO exploit.tblbuffer SELECT * FROM mes4.tblbuffer;

-- 2. Tables liées (Niveau 2)
INSERT INTO exploit.tblorderpos SELECT * FROM mes4.tblorderpos;
INSERT INTO exploit.tblbufferpos SELECT * FROM mes4.tblbufferpos;
INSERT INTO exploit.tblpalletpos SELECT * FROM mes4.tblpalletpos;
INSERT INTO exploit.tblfinstep SELECT * FROM mes4.tblfinstep;

-- 3. Tables de rapports et erreurs (Logs)
INSERT INTO exploit.tblpartsreport SELECT * FROM mes4.tblpartsreport;
INSERT INTO exploit.tblmainterror SELECT * FROM mes4.tblmainterror;
INSERT INTO exploit.tblmachinereport SELECT * FROM mes4.tblmachinereport;