CREATE DATABASE nirctc;

CREATE TABLE users(
    uid int not null primary key,
    mail varchar(50) not null,
    password varchar(50) not null
);

CREATE TABLE train(
    trainno char(6) not null primary key,
    trainname varchar(30) not null unique,
    source varchar(20) not null,
    destination varchar(20) not null,
    general int,
    sleeper int,
    ac1 int,
    ac2 int,
    ac3 int
);

CREATE TABLE ticket(
    pid int not null primary key auto_increment,
    pnr char(10) not null unique,
    pname varchar(30) not null,
    page int not null,
    padhar char(12) not null,
    trainno char(6) not null,
    uid int not null,
    confirmed boolean not null,
    traveldate date not null,
    type_1 varchar(7) not null,
    type_2 char(1)
);