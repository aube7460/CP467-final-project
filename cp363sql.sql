Create database cp363inventorymanagement;
Use cp363inventorymanagement;

Create table Warehouses(wno int(2), location varchar(30), primary key (wno));

insert into Warehouses values(01, 'Markham');
insert into Warehouses values(02, 'Toronto');
insert into Warehouses values(03, 'Waterloo');
insert into Warehouses values(04, 'Burnaby');
insert into Warehouses values(05, 'Surrey');
insert into Warehouses values(06, 'Richmond');

Create table Suppliers(snum int(3), sname varchar(20), wno int(2), primary key (snum), foreign key (wno) references Warehouses (wno));

insert into Suppliers values(001, 'Outtel', 01);
insert into Suppliers values(002, 'AMD', 04);
insert into Suppliers values(003, 'Envidia', 01);
insert into Suppliers values(004, 'ASOOS', 05);
insert into Suppliers values(005, 'Megabyte', 06);
insert into Suppliers values(006, 'ISM', 02);
insert into Suppliers values(007, 'aVGA', 03);


Create table Products(upc varchar(12), pname varchar(50), price decimal(5, 2), quantity int(3), snum int(3), primary key (upc), foreign key (snum) references Suppliers (snum));

insert into Products values('123701235816', 'Core i7 3770k', 319.99, 70, 001);
insert into Products values('571082302375', 'Core i5 3570k', 219.99, 160, 001);
insert into Products values('470128302103', 'Core i7 4770k', 339.99, 260, 001);
insert into Products values('370217302144', 'Core i5 4670k', 299.99, 400, 001);
insert into Products values('103720461023', 'FX-9590', 299.99, 25, 002);
insert into Products values('120370577210', 'FX-8350', 219.99, 350, 002);
insert into Products Values('470127301421', 'R9 290X Windforce', 459.99, 47, 005);
insert into Products values('470123702130', 'R9 290X DirectCU II', 499.99, 50, 004);
insert into Products values('412038201558', 'GTX980 STRIX', 729.99, 80, 004);
insert into Products values('480421803201', 'R9 290 Twin Frozr IV', 399.99, 69, 006);
insert into Products values('217302170401', 'GTX970 Superclocked', 449.99, 150, 007);

Create table Customers(cno int(4), email varchar(40), cname varchar(30), phone varchar(10), address varchar(50), primary key (cno));

Insert into Customers values(0001, 'jligajl@gjajf.com', 'Jglia Jaois', '4091850954', '123 fjoidas st, ajdlag, ON');
Insert into Customers values(0002, 'aljisda@aoisf.com', 'Fasds Gdsafg', '4919491569', '8601 Jaohif Blvd., Ajigaejoi, BC');
insert into Customers values(0003, 'fjalsidj@jfjlsa.com', 'JFdsa Uqpw', '4910591860', '1039 Fsalijd St., Fjdsla, ON');

Create table Orders(invoice int(6), date date, trackingnum varchar(20), cno int(4), primary key (invoice), foreign key (cno) references Customers (cno));

insert into Orders values(000001, '2015-04-05', '081890DAS01038AAHD01', 0001);
insert into Orders values(000002, '2015-05-10', '90AD90F0UAH0ADSHUKDA', 0003);
Insert into Orders values(000003, '2015-02-19', '90ADS0AVG90UGAD90SA0', 0001);

Create table shipin(snum int(3), upc varchar(12), foreign key (snum) references Suppliers (snum), foreign key (upc) references Products (upc) ON DELETE CASCADE ON UPDATE CASCADE);

Create table shipout(wno int(2), invoice int(6), foreign key (wno) references Warehouses (wno), foreign key (invoice) references Orders (invoice));

Create table contain(upc varchar(12), invoice int(6), quantity int(2), foreign key (upc) references Products (upc) ON DELETE CASCADE ON UPDATE CASCADE, foreign key (invoice) references Orders (invoice));
insert into contain values('123701235816', 000002, 2);
insert into contain values('412038201558', 000002, 3);
insert into contain values('103720461023', 000001, 1);
insert into contain values('470127301421', 000003, 2);

Create table place(invoice int(6), cno int(4), foreign key (invoice) references Orders (invoice), foreign key (cno) references Customers (cno));