from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt    # CSRF Token Ignore in post reqs
from django.shortcuts import redirect
from django.urls import reverse
import json
import psycopg2
import random

class authentication():

    @csrf_exempt
    def testing(request):
        return HttpResponse("Test works")

    @csrf_exempt
    def signup(request):

        if request.method == 'GET':
            #form = Signup_form()
            #context = {'form' : form}
            context = {}
            return render(request,'signup.html',context)

        elif request.method == 'POST':
            try:
                conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                cur = conn.cursor()
            except:
                print("Unable to connect to the database")
                return HttpResponse("Unable to connect to the database")   

            
            form_string = request.body.decode('utf-8')
            fields = form_string.split('&')
            username = fields[0].split('=')[1]
            password = fields[1].split('=')[1]
            phoneno = fields[2].split('=')[1]
            print(f"Username --> {username} and Password --> {password} and Phoneno --> {phoneno}")
            
            '''
            form = Signup_form(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                phoneno = form.cleaned_data['phoneno']
                print("Working")
            '''

            if(username and password and phoneno):
                cur.execute(f"SELECT * FROM customer where phone_no = %s",(phoneno,)) 
                row = cur.fetchone()    # Row is a tuple of attributes

                if row is not None:
                    print(row)
                    return HttpResponse("User already exists with same Phone no")

                cur.execute("""INSERT INTO customer (username,password,phone_no) VALUES (%s,%s,%s);""",(username,password,phoneno,))
                conn.commit()
                cur.close()
                conn.close()
                return HttpResponse("Inserted Successfully")
            else:
                cur.close()
                conn.close()
                return HttpResponse("Fields not submitted properly")
            
        else:
            return HttpResponse("METHOD NOT ALLOWED")
                
    @csrf_exempt
    def signin(request,**kwargs):
        if request.method == 'GET':
            if request.session.has_key('phoneno'):

                phoneno = request.session['phoneno']
                context = {'phoneno' : phoneno}
                return render(request,'home.html',context)

            else:
                print("Here")
                print(kwargs)
                return render(request,'signin.html',kwargs)

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
                query = f"SELECT customer_id,username FROM customer where phone_no = %s and password = %s"
                #print(query)
                cur.execute(query,(phoneno,password))
                row = cur.fetchone()
                if row is not None:
                    print(row)
                    cur.close()
                    conn.close()
                    #request.session.set_expiry(300)
                    request.session['phoneno'] = phoneno
                    response = redirect('/home/')
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
            del request.session['phoneno']
            return HttpResponse("<strong>Logged out Successfully.</strong>")
        except:
            print("Logout not Work!!!")
            return HttpResponse("<strong>Failure in Logging out.</strong>")


class customer_view():

    def home(request):
        if request.method == 'GET':
            if request.session.has_key('phoneno'):

                phoneno = request.session['phoneno']
                context = {'phoneno' : phoneno}

                return render(request,'home.html',context)
            else:
                #context = {'error' : 'Sign In Please'}
                return redirect('/signin/')
        else:
            return HttpResponse('METHOD NOT ALLOWED')

    

    @csrf_exempt
    def reservation(request):
        if request.method == 'GET':
            if request.session.has_key('phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")

                #phoneno = request.session['phoneno']
                #context = {'phoneno' : phoneno}

                phoneno = request.session['phoneno']
                print(type(phoneno))
                cur.execute(f"select customer_id from customer where phone_no = '{phoneno}'")
                customer_id = str(cur.fetchone()[0])
                print(customer_id)
                
                cur.execute(f"select * from reservation where customer_id = %s and reservation_status = %s",(customer_id,'inprogress'))
                rows = cur.fetchall()
                print(rows)
                if(len(rows) >= 3):
                    return HttpResponse("Not allowed to have more than 3")

                query = "SELECT name,location FROM outlet"
                cur.execute(query)
                rows = cur.fetchall()

                rows = [i[0] +', '+ i[1] for i in rows]
                context = {'outlets' : rows}

                cur.close()
                conn.close()

                return render(request,'reservation.html',context)
            else:
                #context = {'error' : 'Sign In Please'}
                #text = 'You must be signed in'
                return redirect('/signin/')

        elif request.method == 'POST':
            if request.session.has_key('phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")   

                '''
                reservation_string = request.body.decode('utf-8')
                print(reservation_string)
                fields = reservation_string.split('&')
                v_t_d = fields[0].split('=')[1]
                e_r_d = fields[1].split('=')[1]
                outlet_name = fields[2].split('=')[1]
                print(outlet_name)
                '''
                v_t_d = request.POST.get('Veh_take_date')
                e_r_d = request.POST.get('exp_ret_date')
                outlet_name = request.POST.get('outlet')

                if(v_t_d and e_r_d and outlet_name):
                    outlet = outlet_name.split(",")[0]
                    print(outlet)
                    query1 = f"SELECT outlet_id FROM outlet where name = '{outlet}'"
                    cur.execute(query1)
                    row = cur.fetchone()
                    outlet_id = str(row[0])
                    
                    query = f"SELECT plate_number FROM vehicle where outlet_id = %s and vehicle_status = %s"

                    cur.execute(query,(outlet_id,'not-taken'))
                    rows = cur.fetchall()
                    #print(rows)
                    rows = [i[0] for i in rows]
                    cur.close()
                    conn.close()
                    context = {'vehicle_list' : rows , 'v_t_d' : v_t_d , 'e_r_d' : e_r_d , 'outlet_name' : outlet}
                    return render(request,'vehicle.html',context = context)
                    
                    #return HttpResponse("U gave values")

                else:
                    cur.close()
                    conn.close()
                    return HttpResponse("fields not submitted properly")
                #print(f"Username --> {username} and Password --> {password} and Phoneno --> {phoneno}")

            else:
                return HttpResponse('METHOD NOT ALLOWED')

    @csrf_exempt
    def vehicle_submission(request):
        if request.method == 'POST':
            if request.session.has_key('phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")

                v_t_d = request.POST.get('v_t_d')
                e_r_d = request.POST.get('e_r_d')
                plate_no = request.POST.get('plate-no')
                outlet = request.POST.get('outlet')
                reservation_date = '2001-12-20'     # Should be date/time of taking reservation
                reservation_status = 'inprogress'
                advance = 1000

                phoneno = request.session['phoneno']
                cur.execute(f"select customer_id from customer where phone_no = '{phoneno}'")
                customer_id = str(cur.fetchone()[0])

                cur.execute(f"select employee_id from employee")
                employee_id_list = [i[0] for i in cur.fetchall()]
                #print(employee_id_list)
                #print(outlet)
                cur.execute(f"SELECT outlet_id FROM outlet where name = '{outlet}'")
                row = cur.fetchone()
                outlet_id = str(row[0])

                random_employee_id = random.choice(employee_id_list)

                reservation_insert_query = f'INSERT INTO reservation (reservation_date,vehicle_taken_date,expected_return_date,advance,reservation_status,customer_id,emp_id,outlet_id,plt_no_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'

                cur.execute(reservation_insert_query,(reservation_date,v_t_d,e_r_d,advance,reservation_status,customer_id,random_employee_id,outlet_id,plate_no,))
                conn.commit()

                query_update = f"update vehicle set vehicle_status='selected' where plate_number='{plate_no}';"
                cur.execute(query_update)
                conn.commit()

                cur.close()
                conn.close()
                return HttpResponse("Inserted reservation success :)")

            else:
                return HttpResponse("Sign in pls :(")

        else:   
            return HttpResponse("METHOD NOT ALLOWED")

    @csrf_exempt
    def view_reservations(request):
        if request.method == 'GET':
            if request.session.has_key('phoneno'):
                try:
                    conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                    cur = conn.cursor()
                except:
                    print("Unable to connect to the database")
                    return HttpResponse("Unable to connect to the database")

                phoneno = request.session['phoneno']
                cur.execute(f"select customer_id from customer where phone_no = '{phoneno}'")
                customer_id = str(cur.fetchone()[0])


                query = f"SELECT reservation_date,vehicle_taken_date,expected_return_date,reservation_status,plt_no_id from reservation where customer_id = '{customer_id}'"
                cur.execute(query)
                rows = cur.fetchall()
                

                cur.close()
                conn.close()

                context = {'phoneno':phoneno , 'reservations' : rows}

                return render(request,'view_reservations.html',context = context)

            else:
                return HttpResponse("Sign in pls :(")
        else:
            return HttpResponse("METHOD NOT ALLOWED")
'''
    def vehicle(request):
        if request.session.has_key('phoneno'):
            try:
                conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
                cur = conn.cursor()
            except:
                print("Unable to connect to the database")
                return HttpResponse("Unable to connect to the database")

            print("Working here")
            #for key, value in kwargs.items():
            #    print("%s == %s" %(key, value))

            outlet = outlet_name.split(",")[0]

            query = 'SELECT plate_number FROM vehicles where outlet_name = %s'

            cur.execute(query,(outlet))
            rows = cur.fetchall()
            print(rows)

            cur.close()
            conn.close()

            context = {'outlet': list_of_vehicles}
            return HttpResponse("WOrking")
'''

# phoneno = request.session['phoneno']
# select customer_id from customer where phone_no = phoneno