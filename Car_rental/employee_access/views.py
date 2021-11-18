from django.shortcuts import render

class authentication():

    @csrf_exempt
    def testing(request):
        return HttpResponse("Test works")

    @csrf_exempt
    def signin(request):
        if request.method == 'GET':
            if request.session.has_key('emp_phoneno'):

                #phoneno = request.session['phoneno']
                #context = {'phoneno' : phoneno}
                #return render(request,'home.html',context)
                return HttpResponse("Signed in :)")

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
                    #response = redirect('/home/')
                    return HttpResponse("123WORKS")
    
                cur.close()
                conn.close()
                return HttpResponse("Wrong username or password")
            else:
                cur.close()
                conn.close()
                return HttpResponse("Fields not submitted properly")

        else:
            return HttpResponse("METHOD NOT ALLOWED")
# Create your views here.
