from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt    # CSRF Token Ignore in post reqs
from django.shortcuts import redirect
from django.urls import reverse
import json
import psycopg2
from .forms import Signup_form

class authentication():


    def testing(request):
        conn = psycopg2.connect("dbname='trial_db' user='postgres' host='localhost' password='trial@123'")
        cur = conn.cursor()

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
                
                query = f"SELECT plate_number FROM vehicle where outlet_id = %s"

                cur.execute(query,(outlet_id))
                rows = cur.fetchall()
                print(rows)
                cur.close()
                conn.close()
                context = {'vehicle_list' : rows , 'v_t_d' : v_t_d , 'e_r_d' : e_r_d}
                return render(request,'vehicle.html',context = context)
                
                #return HttpResponse("U gave values")

            else:
                cur.close()
                conn.close()
                return HttpResponse("fields not submitted properly")
            #print(f"Username --> {username} and Password --> {password} and Phoneno --> {phoneno}")

        else:
            return HttpResponse('METHOD NOT ALLOWED')

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