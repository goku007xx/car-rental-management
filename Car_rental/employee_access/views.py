from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import redirect
import json
import psycopg2
import random

from datetime import datetime as dt

class authentication():

    @csrf_exempt
    def testing(request):
        return HttpResponse("Test works")

    @csrf_exempt
    def signin(request):
        if request.method == 'GET':
            if request.session.has_key('emp_phoneno'):

                phoneno = request.session['emp_phoneno']
                context = {'phoneno' : phoneno}
                #return render(request,'ehome2.html',context)
                resp = redirect('/employee/home/')
                return resp
                #return HttpResponse("Signed in :)")

            else:
                return render(request,'esignin.html')

        elif request.method == 'POST':
            try:
                conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                cur = conn.cursor()
            except:
                print("Unable to connect to the database")
                return HttpResponse("Unable to connect to the database")

            form_string = request.body.decode('utf-8')
            fields = form_string.split('&')
            phoneno = fields[0].split('=')[1]
            password = fields[1].split('=')[1]

            if(phoneno and password):
                query = f"SELECT employee_id,employee_name FROM employee where employee_phone_no = %s and employee_password = %s"
                #print(query)
                cur.execute(query,(phoneno,password))
                row = cur.fetchone()
                if row is not None:
                    print(row)
                    cur.close()
                    conn.close()
                    #request.session.set_expiry(300)
                    request.session['emp_phoneno'] = phoneno
                    response = redirect('/employee/home/')
                    return response
    
                cur.close()
                conn.close()
                return HttpResponse("Wrong username or password")
            else:
                cur.close()
                conn.close()
                return HttpResponse("Fields not submitted properly")

        else:
            return HttpResponse("METHOD NOT ALLOWED")

    def logout(request):
        try:
            del request.session['emp_phoneno']
            return HttpResponse("<strong>Employee Logged out Successfully.</strong>")
        except:
            print("Logout not Work!!!")
            return HttpResponse("<strong>Failure in Logging out.</strong>")
# Create your views here.

class employee_view():
    
    def home(request):
        if request.method == 'GET':
            if request.session.has_key('emp_phoneno'):

                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")
                
                phoneno = request.session['emp_phoneno']

                context={"phoneno":phoneno}
                        #"reservations":rows
                    #request.session.set_expiry(300)
                
                return render(request, 'ehome.html', context)
                #phoneno = request.session['emp_phoneno']
                #context = {'phoneno' : phoneno}

                #return render(request,'ehome.html',context)
            else:
                #context = {'error' : 'Sign In Please'}
                return redirect('/employee/signin/')
        else:
            return HttpResponse('METHOD NOT ALLOWED')

    @csrf_exempt
    def view_res(request):
        if request.method =='GET':
            if request.session.has_key('emp_phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")

            phoneno = request.session['emp_phoneno']

            query = f"SELECT employee_id,employee_name FROM employee where employee_phone_no ='{phoneno}'"
            #print(query)
            cur.execute(query)
            row = cur.fetchone()

            emp_id = row[0]

                
            print("emp:",row)
            query = f"SELECT reservation_date,vehicle_taken_date,expected_return_date,plt_no_id,customer_id,reservation_id from reservation where emp_id = '{emp_id}' and reservation_status='inprogress'"
            cur.execute(query)
            rows = cur.fetchall()
            print(rows)

            context = {'phoneno' : phoneno , 'reservations' : rows}

            return render(request,'view_res.html',context = context)
        else:
            HttpResponse('METHOD NOT ALLOWED')


    def view_approve(request):
        if request.method =='GET':
            if request.session.has_key('emp_phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")

            phoneno = request.session['emp_phoneno']

            query = f"SELECT employee_id,employee_name FROM employee where employee_phone_no ='{phoneno}'"
            #print(query)
            cur.execute(query)
            row = cur.fetchone()

            emp_id = row[0]
            print('empid',row)
            
            print("HereVie")

            query = f"select reservation_id from reservation where emp_id = '{emp_id}' and reservation_status='approved' order by customer_id"
            cur.execute(query)
            rows = cur.fetchall()
            print(rows)

            rows = [i[0] for i in rows]
            print(rows)
            print("HereVie2")


            rents =[] 
            for res_id in rows:
                query = f"SELECT bill_id , taken_date , return_date  , total_amt , refund , customer_id , plt_no_id , reservation_id from rent where reservation_id={res_id}"
                cur.execute(query)
                rent_row = cur.fetchone()
                print(rent_row)
                rents.append(rent_row)

            print(rents)
            print("HereVie3")

            conn.close()

            print(rents)
            context = {'phoneno' : phoneno , 'rents' : rents}
            
            return render(request,'view_approve.html',context = context)
        else:
            print("METHOD NOT ALLOWED")



    @csrf_exempt
    def cancel_reservation(request):
        if request.method =='POST':
            if request.session.has_key('emp_phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")

                body = json.loads(request.body)
                res_id = body['id']
                print(res_id)

                query = f"select plt_no_id from reservation where reservation_id='{res_id}'"
                cur.execute(query)
                row = cur.fetchone()
                plate_no = row[0]
                print(plate_no)
                print("Here")

                query_update = f"update vehicle set vehicle_status='not-taken' where plate_number='{plate_no}';"
                cur.execute(query_update)
                conn.commit()

                print("Here2")

                query_delete = f"delete from reservation where reservation_id='{res_id}';"
                cur.execute(query_delete)
                conn.commit()

                print('Here3')
                conn.close()

                
                return HttpResponse("Works1")
                #return redirect('/employee/home/')

            else:
                return redirect('/employee/signin/')
        else:
            return HttpResponse("METHOD NOT ALLOWED")


    @csrf_exempt
    def approve_reservation(request):
        if request.method =='POST':
            if request.session.has_key('emp_phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")

                body = json.loads(request.body)
                res_id = body['id']
                print("res:",res_id)

                phoneno = request.session['emp_phoneno']

                query = f"select plt_no_id, vehicle_taken_date , expected_return_date , advance, customer_id from reservation where reservation_id='{res_id}'"
                cur.execute(query)
                row = cur.fetchone()
                plate_no = row[0]

                v_t_d = row[1]
                e_r_d = row[2]
                advance = row[3]
                cust_id = row[4]

                print(plate_no,v_t_d, e_r_d, advance, cust_id)

                query = f"SELECT employee_id,employee_name FROM employee where employee_phone_no ='{phoneno}'"
                #print(query)
                cur.execute(query)
                row = cur.fetchone()

                emp_id = row[0]

                print("HereA0")
                # TAKEN means vehicle not in outlet, taken and gone
                query_update = f"update vehicle set vehicle_status='taken' where plate_number='{plate_no}';"
                cur.execute(query_update)
                conn.commit()

                print("HereA")


                # APPROVED Means bill generated and will wait for car to come back
                query_update = f"update reservation set reservation_status='approved' where reservation_id='{res_id}';"
                cur.execute(query_update)
                conn.commit()

                print("HereA2")
                # generate default bill
                rent_insert_query = f'INSERT INTO rent (taken_date , return_date , no_of_days , tax_amt , total_amt , refund , customer_id , plt_no_id , reservation_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'

                
                num_days = (e_r_d - v_t_d).days
                refund = advance
                
                # CAN query model type and AC/no AC and do if else for base amount (WHICH GURU KIRAN WILL DO(MUST DO!))
                amt = 1000
                cur.execute(rent_insert_query,(v_t_d.strftime('%d-%m-%Y'), e_r_d.strftime('%d-%m-%Y'), num_days , 200, num_days*amt ,refund,cust_id,plate_no,res_id))
                conn.commit()
                conn.close()

                print("HereA3")

                return HttpResponse("Works1")

            else:
                return redirect('/employee/signin/')
        else:
            return HttpResponse("METHOD NOT ALLOWED")