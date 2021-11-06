\c car_rental_management

--1) update income of outlet from reservation completed  ;

    -- Assume outlet id is passed as parameter

update outlet
set outlet_savings = outlet_savings+(
    select sum(total_amount) from rent 
    where outlet_id=1 and reservation_id in (
        select reservation_id
        from reservation
        where reservation_status='completed'
    ) 
)
where outlet_id=1;

select * from outlet;



--2) getting final payment amount bill by joining the rent and got_discount;

    --  DID NOT UPDATE THE TOTAL AMOUNT INSTEAD JUST RETURNED THE AMOUNT

        -- for bill_id=1

        insert into got_discount values('JollySeason',1);
        
        SELECT * from got_discount;
    
    
    select total_amount+tax_amount - (
        select sum(discount_amount)
        from discount
        where promo_id in (
            select disc_id
            from got_discount
            where bill_id=1
        )
    ) as payable
    from rent
    where bill_id = 1;


--3) finding the customer with maximum rent amount using max aggrigation group by outlet;

    -- reservation is based on outlet wise, using reserervation fk, get the max amount through rent table

    
    select * from rent;
    select * from reservation;

    select foo.outlet_id, rent.customer_id, foo.max
    from (
        select outlet_id,max(total_amount)
        from reservation join rent on rent.reservation_id=reservation.reservation_id
        group by outlet_id
        ) as foo join  rent on rent.total_amount=foo.max;

    
-- 4)finding the customer with most number of reservations;

    select customer_id,count(*)
    from reservation
    group by customer_id;

-- 5)selecting customer who has made reservation for all cars of an outlets;
                        -- for all , using double negation
        
        -- assume outlet 2
            -- to check
        select plate_number,outlet_id
        from vehicle;

            
        select customer_id,plt_num,outlet_id
        from reservation;
    
    select customer_id, licence_number
    from customer
    where NOT EXISTS (
        (
            Select plate_number
            from vehicle
            where outlet_id=2
        )
        EXCEPT
        (
            SELECT plt_num
            from reservation
            where customer.customer_id=reservation.customer_id
        )
    );