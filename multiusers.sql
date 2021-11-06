\c car_rental_management

--creating views for customer role
create view customer_view_outlet as select outlet_id,outlet_name,outlet_location from outlet;

create view customer_view_vehicle as select plate_number,outlet_id,model,number_of_seats,ac from vehicle;

create view customer_view_reservation as select reservation_id,reservation_date,vehicle_taken_date,expected_return_date,customer_id,outlet_id,advance,plt_num,reservation_status from reservation;

create view customer_view_rent as select * from rent;

create view customer_view_outlet_contact as select * from outlet_contact;

--customer role creation and granting the views to customer role

DROP ROLE IF EXISTS customer_role; 

create role customer_role with password 'qwerty';

grant select on customer_view_outlet to customer_role;

grant select on customer_view_vehicle to customer_role;

grant select,insert on customer_view_reservation to customer_role;

grant select on customer_view_rent to customer_role;

grant select on customer_view_outlet_contact to customer_role;


--creating views for employee role

create view employee_view_customer as select * from customer;

create view employee_view_outlet as select outlet_id,outlet_name,outlet_location from outlet;

create view employee_view_vehicle as select * from vehicle;

create view employee_view_reservation as select * from reservation;

create view employee_view_outlet_contact as select * from outlet_contact;

--employee role creation and granting view to employee role

DROP ROLE IF EXISTS employee_role; 

create role employee_role with password 'qwerty';

grant select on employee_view_customer to employee_role;

grant select on employee_view_outlet to employee_role;

grant select,insert,update,delete on employee_view_vehicle to employee_role;

grant select,update,delete on employee_view_reservation to employee_role;

grant select on employee_view_outlet_contact to employee_role;


--creating views of admin role

create view admin_view_customer as select * from customer;

create view admin_view_outlet as select * from outlet;

create view admin_view_employee as select * from employee;

create view admin_view_vehicle as select * from vehicle;

create view admin_view_reservation as select * from reservation;

create view admin_view_rent as select * from rent;

create view admin_view_discount as select * from discount;

create view admin_view_outlet_contact as select * from outlet_contact;

create view admin_view_got_discount as select * from got_discount;

--admin role creation and granting views to admin role

DROP ROLE IF EXISTS admin_role; 

create role admin_role with password 'qwerty';

grant select on admin_view_customer to admin_role;

grant select on admin_view_outlet to admin_role;

grant select,insert,update,delete on admin_view_employee to admin_role;

grant select,insert,update,delete on admin_view_vehicle to admin_role;

grant select on admin_view_reservation to admin_role;

grant select on admin_view_rent to admin_role;

grant select,insert,update,delete on admin_view_discount to admin_role;

grant select,update on admin_view_outlet_contact to admin_role;

grant select on admin_view_got_discount to admin_role;


--creating customer, employee, admin users
DROP USER IF EXISTS customer_user1;

create user customer_user1 with password '123';

DROP USER IF EXISTS employee_user1;

create user employee_user1 with password '123';

DROP USER IF EXISTS admin_user1;

create user admin_user1 with password '123';

--granting roles to each users

grant customer_role to customer_user1;

grant employee_role to employee_user1;

grant admin_role to admin_user1;


