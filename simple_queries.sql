
\c car_rental_management

-- CUSTOMER VIEW

-- 1) list of all outlets - select * from outlet;s1

select outlet_name,outlet_location
from outlet;


-- 2) list of available vehicles - ASSUME checking in outlet_id=2
            -- LATER can be passed parameter in function
select * from vehicle 
where vehicleStatus='not-taken' and outlet_id=2;


-- 3) list of reservations made by customer -  ASSUME customer_id=1
                -- LATER can be passed as a parameter
select * from reservation where customer_id=1;


-- 4) when the customer selects the vehicle then the status of the vehicle is set to 

    -- to show list of not-taken
    select * from vehicle where vehicleStatus='not-taken';

update vehicle 
set vehicleStatus='selected' 
where plate_number='KA-18-1221' and vehicleStatus='not-taken';

    -- to show update
    select * from vehicle where plate_number='KA-18-1221';

        -- CAN DO concurrency control here


-- 5) getting outlet contact

select outlet_mail,outlet_phone from outlet_contact where outlet_id=1;


-- ________________________________________________________________________


-- EMPLOYEE VIEW

-- 1) list of all vehicles in that outlet - 
select * from vehicle where outlet_id=1;

-- 2) list of all reservations made my all customers in that outlet, 
        -- to see if to approve a customer coming to outlet on pickup date
select * from reservation where outlet_id=1 and reservation_status='inprogress';

-- 3) update rent table, where reservations whose approves is inprogress
        -- set the reservation status to returned, and update the rent 

    -- first set return_date(REAL) in rent, when customer comes back
    update rent
    set return_date='20-01-2021',number_of_days=return_date-taken_date,total_amount=1000*number_of_days+tax_amount
    where reservation_id=1;

    select * from rent where reservation_id=1;

    -- now in reservation go and set status to returned + vehicle status to 'not-taken'

    update reservation
    set reservation_status='completed'
    where reservation_id=1;

        select * from reservation where reservation_id=1;

    update Vehicle
    set vehicleStatus='not-taken'
    where plate_number = (SELECT plt_num from reservation where reservation_id=1);

        SELECT * from vehicle where plate_number = (SELECT plt_num from reservation where reservation_id=1);

-- 4) IF customer shows usp on pickup date in reservation
            -- insert into rent table

            -- dummy to show
                INSERT into reservation values(3, '21-04-2021', '28-04-2021','01-05-2021',2,1,1000,1,'DW-12-2192','inprogress');

        insert into rent(taken_date, return_date ,number_of_days ,total_amount, customer_id ,reservation_id ,refund ,plt_num )
        select vehicle_taken_date,expected_return_date,expected_return_date-vehicle_taken_date,1000*(expected_return_date-vehicle_taken_date), customer_id,reservation_id ,advance*0.1 , plt_num
        from reservation
        where reservation_id=3;

                select * from rent where reservation_id=3;


            -- as he showed up update vehicle status to taken

        update Vehicle
        set vehicleStatus='taken'
        where plate_number = (SELECT plt_num from reservation where reservation_id=3);

        SELECT * from vehicle where plate_number = (SELECT plt_num from reservation where reservation_id=3);


-- ____________________________________________________________________________________________

-- MANAGER/ADMIN VIEW

--1) view current savings of an outlet (after adding base + income of any rent(complex query))  - 
select outlet_savings from outlet where outlet_id=1;      

--2) list of all vehicles in that outlet - 
select * from vehicle where outlet_id=1;

--3) orderby(number of seats, outlet) all vehicles in db 

select number_of_seats, plate_number, model,outlet_id
from vehicle
order by number_of_seats;

--4) update outlet contact

update outlet_contact
set outlet_mail='ilikeWeed@cubahavana',outlet_phone='0212112123'
where outlet_id=1;

    select * from outlet_contact where outlet_id=1

