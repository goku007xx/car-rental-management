from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import redirect
import json
import psycopg2
import random

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

                
            print(row)
            query = f"SELECT reservation_date,vehicle_taken_date,expected_return_date,plt_no_id,customer_id,reservation_id from reservation where emp_id = '{emp_id}' and reservation_status='inprogress'"
            cur.execute(query)
            rows = cur.fetchall()
            print(rows)

            context = {'phoneno' : phoneno , 'reservations' : rows}

            return render(request,'view_res.html',context = context)

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

                print("Here3")
                phoneno = request.session['emp_phoneno']

                query = f"SELECT employee_id,employee_name FROM employee where employee_phone_no ='{phoneno}'"
                    #print(query)
                cur.execute(query)
                row = cur.fetchone()

                emp_id = row[0]


                query = f"SELECT reservation_date,vehicle_taken_date,expected_return_date,plt_no_id,customer_id,reservation_id from reservation where emp_id = '{emp_id}' and reservation_status='inprogress'"
                cur.execute(query)
                rows = cur.fetchall()

                context = {'phoneno' : phoneno , 'reservations' : rows}
                cur.close()
                conn.close()
                print("Here4")

                return HttpResponse("Works1")
                #return redirect('/employee/home/')

            else:
                return redirect('/employee/signin/')
        else:
            return HttpResponse("METHOD NOT ALLOWED")
