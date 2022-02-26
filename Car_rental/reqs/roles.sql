create role customer_role;
grant select,insert on customer to customer_role;
grant select,update on vehicle to customer_role;
grant select,insert on reservation to customer_role;
grant select on outlet to customer_role;
grant select on employee to customer_role ;
create user customer with password '123';
grant customer_role to customer;

create role employee_role;
grant select on employee to employee_role;
grant select on customer to employee_role;
grant select,update on reservation to employee_role;
grant select,insert,update on rent to employee_role;
grant select,insert,update,delete on reservation to employee_role;
grant select,update on vehicle to employee_role;
grant select,update on outlet to employee_role;
create user employee with password '456';
grant employee_role to employee;

grant select,update on outlet,customer_customer_id_seq ,reservation_reservation_id_seq,employee_employee_id_seq,employee_employee_id_seq,outlet_outlet_id_seq,rent_bill_id_seq,outlet_contact to customer_role;
grant select,update on outlet,customer_customer_id_seq ,reservation_reservation_id_seq,employee_employee_id_seq,employee_employee_id_seq,outlet_outlet_id_seq,rent_bill_id_seq,outlet_contact to employee_role;
