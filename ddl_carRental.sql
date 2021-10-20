drop database car_rental_management;
create database car_rental_management;

\c car_rental_management

create table customer ( 
Customer_id int NOT NULL,
Customer_phoneno char(12) NOT NULL,
Aadhar char(12) NOT NULL,
Driving_licence_no char(12) NOT NULL,
Customer_addr varchar NOT NULL,
Primary key(customer_id)
);


create table outlet ( 
Outlet_id int NOT NULL,
Outlet_name varchar NOT NULL,
Outlet_tax int NOT NULL,
Primary key(Outlet_id)
);

create table reservation ( 
Reservation_id int NOT NULL,
Reservation_date DATE NOT NULL,
Expected_return_date DATE NOT NULL,
Vehicle_taken_date DATE NOT NULL,
Customer_id int NOT NULL,
Outlet_id int NOT NULL,
Approves boolean NOT NULL,
Primary key(Reservation_id),
Foreign key(Customer_id) references Customer(Customer_id),
Foreign key(Outlet_id) references Outlet(Outlet_id)
);


create table vehicle( 
Vehicle_id int NOT NULL,
Registration_no CHAR(20) NOT NULL,
Vehicle_status varchar NOT NULL,
Outlet_id int NOT NULL,
Foreign key(Outlet_id) references Outlet(Outlet_id),
Primary key(Registration_no)
);

create table vehicle_type( 
No_of_seats int NOT NULL,
Name varchar NOT NULL,
Vehicle_model varchar NOT NULL,
Charge_per_hour int NOT NULL,
Reservation_id int NOT NULL,
Registration_no CHAR(20) NOT NULL,
Foreign key(Reservation_id) references Reservation(Reservation_id),
Foreign key(Registration_no) references Vehicle(Registration_no),
Primary key(Registration_no,reservation_id,no_of_seats)
);


create table rent(
Bill_id int NOT NULL,
Taken_date DATE NOT NULL,
Return_date DATE NOT NULL,
Days int NOT NULL,
Tax_amount int NOT NULL,
Total_amt int NOT NULL,
Customer_id int NOT NULL,
Primary key(Bill_id),
Foreign key(Customer_id) references Customer(Customer_id)
);

create table discount(
Discount_type char(30) NOT NULL,
Percentage int NOT NULL,
Primary key(Discount_type)
);

create table outletContact(
Outlet_id int NOT NULL,
Outlet_phone varchar(12) NOT NULL,
Foreign key(Outlet_id) references outlet(outlet_id)
);




