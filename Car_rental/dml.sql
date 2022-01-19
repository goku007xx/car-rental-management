\c trial_db

INSERT into outlet values(1, 'Vinayaka outlets', 'bangalore',10000),(2,'narayan outlets','chitradurga',20000);

INSERT into vehicle values('DA-12-2192','omni',6,TRUE,'taken',500,1),('KA-18-1221','swift',5,TRUE,'not-taken',1000,2),('DW-12-2192','omni',6,TRUE,'selected',1500,1),('KA-18-1220','fastest',10,TRUE,'not-taken',2500,2);

INSERT into employee(employee_name ,employee_password , employee_phone_no , outlet_id ) values ('Sam', '123', '9123456789', 1),('Ram', '123' ,'8123456789',2);

INSERT into outlet_contact values('9777777777','Vinayaka@gmail.com',1),('9666666666','narayan@gmail.com',2)