drop database if exists e_restaurant;
create database e_restaurant;
use e_restaurant;

create table Item(
	id_item integer unique auto_increment,
    _name varchar(30) not null,
    _type enum('dish', 'drink', 'platter') not null,
    _description varchar(100) unique,
    _price float not null,
    _image varchar(200) not null,
    primary key(id_item)
);

create table Menu(
	id_menu integer unique auto_increment,
    _name char(30),
    _description varchar(70),
    primary key(id_menu)
);

create table Receipt(
	id_receipt integer unique auto_increment,
    date_time datetime,
    _total_amount float,
    primary key(id_receipt)
);

create table Receipt_Item(
	id_receipt integer not null,
    id_item integer not null,
    _amount integer not null,
    primary key(id_receipt, id_item),
    foreign key (id_receipt) references Receipt(id_receipt) on delete cascade,
    foreign key (id_item) references Item(id_item) on delete cascade
);

create table Menu_Item(
	id_menu integer not null,
    id_item integer not null,
    primary key(id_menu, id_item),
    foreign key (id_menu) references Menu(id_menu) on delete cascade,
    foreign key (id_item) references Item(id_item) on delete cascade
);

insert into Item(_name, _type, _description, _price, _image) 
values ('Lomo saltado','dish', 'Un tradicional lomo saltado hecho de riquisimo carne asada, papas fritas y su arroz', 15.00,
'https://www.recetas-venezolanas.com/base/stock/Recipe/205-image/205-image_web.jpg');
insert into Item(_name, _type, _description, _price, _image) 
values ('Fuente','platter', 'Fuente de zenca + Arroz verde + Chuleta de chancho + Pastel de tallarin', 75.00,
'https://media-cdn.tripadvisor.com/media/photo-s/0d/11/b4/a5/delicious-lamb.jpg');
insert into Item(_name, _type, _description, _price, _image) 
values ('Chicha morada','drink', 'Jarra de 3L', 10.00,
'https://www.thespruceeats.com/thmb/yCuLhIlhmAOen6ECm5snuVQNR1Q=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/chicha-morada-4156888-hero-01-f3cb01b1112f4f44a4627de614a8f7b9.jpg');