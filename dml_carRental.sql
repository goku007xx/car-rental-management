\c car_rental_management


INSERT into customer values(1,'9999999999','DL1234','Gurguoan'),(2,'8296498806','KA1234','banashankari');

INSERT into outlet values(1, 'Vinayaka outlets', 'bangalore',10000),(2,'narayan outlets','chitradurga',20000);

insert into employee values(1,'employee 1','5485934854',40000,1),(2,'employee 2','5485934854',45000,1);

INSERT into Vehicle values('DA-12-2192',1,'omni',6,TRUE,'taken'),('KA-18-1221',2,'swift',5,TRUE,'not-taken'),('DW-12-2192',1,'omni',6,TRUE,'selected');

INSERT into reservation values(1, '11-01-2021', '12-01-2021','19-01-2021',1,1,1000,1,'DA-12-2192','inprogress'),(2, '23-01-2021', '25-01-2021','01-02-2021',1,2,1000,2,'KA-18-1221','cancel');

INSERT into rent(taken_date, return_date ,number_of_days ,tax_amount, total_amount, customer_id ,reservation_id ,refund ,plt_num) values('12-01-2021','19-01-2021',7,100,3000,1,1,0,'DA-12-2192'),('12-01-2021','19-01-2021',7,100,3000,1,2,0,'KA-18-1221');

INSERT into discount values('AugustSeason',100,'19-01-2021','29-01-2021'),('JollySeason',399,'29-01-2021','31-03-2021');

INSERT into outlet_contact values(1,'2190301923',NULL),(2,'3435524534','car_rental_management@gmail.com');


insert into got_discount values('AugustSeason',1),('JollySeason',2);