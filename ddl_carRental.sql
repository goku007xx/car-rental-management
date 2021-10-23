drop database car_rental_management;
create database car_rental_management;

\c car_rental_management

create table customer ( 
customer_id int NOT NULL,
mobile_number char(12) NOT NULL,
licence_number char(12) NOT NULL,
customer_address varchar NOT NULL,

Primary key(customer_id)
);

create table outlet ( 
outlet_id int NOT NULL,
outlet_name varchar NOT NULL,
outlet_location varchar NOT NULL,
outlet_contact NOT NULL,

Primary key(outlet_id)
);

create table reservation ( 
reservation_id int NOT NULL,
reservation_date DATE NOT NULL,
vehicle_taken_date DATE NOT NULL,
expected_return_date DATE NOT NULL,
customer_id int NOT NULL,
outlet_id int NOT NULL,
advance int default 1000,

Primary key(reservation_id),
Foreign key(customer_id) references customer(customer_id),
Foreign key(outlet_id) references outlet(outlet_id)
);


create table vehicle( 
vehicle_id int NOT NULL,
plate_number CHAR(20) NOT NULL,
vehicle_status varchar NOT NULL default 'available',
outlet_id int NOT NULL,
model varchar NOT NULL,
number_of_seats int NOT NULL,

Foreign key(outlet_id) references outlet(outlet_id),
Primary key(vehicle_id)
);

create table rent(
bill_id int NOT NULL,
taken_date DATE NOT NULL,
return_date DATE NOT NULL,
number_of_days int NOT NULL taken_date-return_date,
tax_amount int NOT NULL default 10,
total_amount int NOT NULL,
customer_id int NOT NULL,
reservation_id int NOT NULL,////////////////////////////////////
refund int NOT NULL,

Primary key(bill_id),
Foreign key(customer_id) references customer(customer_id),
Foreign key(reservation_id) references reservation(reservation_id)
);

create table discount(
promo_id char(30) NOT NULL,
discount_amount int NOT NULL,
startdate DATE NOT NULL,
enddate DATE NOT NULL,
bill_id int,

Primary key(Discount_type),
Foreign key(bill_id) references rent(bill_id)
);

create table outlet_contact(
outlet_id int NOT NULL,
outlet_phone char(12) NOT NULL,
outlet_mail varchar NOT NULL,

Foreign key(outlet_id) references outlet(outlet_id)
);

create table employee(
    employee_id int NOT NULL,
    employee_name varchar NOT NULL,
    employee_mobile_number char(12) NOT NULL
    employee_salary int NOT NULL,
    outlet_id int NOT NULL,

    Primary key(employee_id),
    Foreign key(outlet_id) references outlet(outlet_id)
)


