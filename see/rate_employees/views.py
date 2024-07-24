

from django.http import HttpResponse
from django.shortcuts import render, redirect
from rate_employees.models import Employee, Evaluation, Designation
from . registrationForm import EmployeeRegistration, NewEmployeeRegistration
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from . import petro
import pandas as pd
import os
from django.db.models import Q


# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request,'employees/homePage.html')

@login_required(login_url='login')
def employees_info(request):
    employee = Employee.objects.all()
    return render (request, 'employees/evaluation.html', {'emp': employee} )

@login_required(login_url='login')
def mark_employees(request):
    return render (request, 'employees/mark.html')

def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method == "POST":
            fm = UserCreationForm(request.POST)
            if fm.is_valid():
                fm.save()
                print("this post from registration")
                return redirect('home')
        else:
            fm = UserCreationForm()
        return render(request,'employees/registration.html',{'form': fm})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                messages.info(request, 'Username or Password is incorrect')

        return render(request,'employees/login.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with new password hash
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
    else:
        print("executed!!")
        form = PasswordChangeForm(request.user)
    
    context = {
               
                'form': form
               
                }
    return render (request,'employees/change_password.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def showProfileData(request):
    #df = pd.read_excel("employees.xlsx")
    #employees_data = df.to_dict(orient='records')
    if request.method == 'POST':

        return redirect('home') # no data will be saved!!!
        print("request post")
        print(request.POST)
        fm = EmployeeRegistration(request.POST)

        if fm.is_valid():
            mydata = Employee.objects.filter(enothi_id = request.user)
            if mydata.exists():
                #update profile
                myProfileData = Employee.objects.get(enothi_id = request.user)
                #print(" My Objects ",myProfileData[0])
                myProfileData.ename = request.POST['name']
                myProfileData.eemail = request.POST['email']
                myProfileData.empid = request.POST['empid']
                myProfileData.edesignation = request.POST['designation']
                myProfileData.esection = -1
                myProfileData.edept = -1
                myProfileData.edivision = request.POST['division']
                myProfileData.edirectorate = -1
                myProfileData.save()
                return redirect('home')

            #print(fm)
            print("This is POST statement")
            print(request.POST['name'])
            name = request.POST['name']
            email = request.POST['email']
            enothi_id = request.user
            empid = request.POST['empid']
            designation = request.POST['designation']
            section = -1
            department = -1
            division = request.POST['division']
            directorate = -1

            new_emp = Employee(empid = empid, enothi_id = enothi_id , ename = name, eemail = email, edesignation = designation, edept = department, esection = section, edivision = division, edirectorate = directorate)
            #print(fm.cleaned_data)
            new_emp.save()
            return redirect('home')
        #else if request.POST['enothi_id']:
        else:
            print("not valid enothi_id ",request.user)
            print("enothi_id from post ",request.POST['enothi_id'])
            #print(fm)

    elif request.method == 'GET' and 'employee_name' in request.GET:
        return redirect('home')
        
        employee_name = request.GET.get('employee_name')
        
        #print(employee_name)
        for employee in employees_data:
            idname = "["+str(employee['ID'])+"] - "+employee['Name']
            
            if idname == employee_name:
                print("got in list")
                print(idname)
                data = {
                    'name':employee['Name'],
                    'designation': employee['Designation'],
                    'division': employee['Department'],
                    'empid' : employee['ID']
                }
    
                return JsonResponse(data)
    elif request.method == 'GET' and 'employee_id' in request.GET:
        return redirect('home')
        
        employee_id = request.GET.get('employee_id')
        
        print("helloooooooooooo")
        print(employee_id)

        for employee in employees_data:
            idname = "["+str(employee['ID'])+"] - "+employee['Name']
            
            if idname == employee_name:
                print("got in list")
                print(idname)
                data = {
                    'name':employee['Name'],
                    'designation': employee['Designation'],
                    'division': employee['Department'],
                    'empid' : employee['ID']
                }
    
                return JsonResponse(data)
    else:

        fm = EmployeeRegistration()
        fm.initial['section'] = -1
        fm.initial['department'] = -1
        fm.initial['directorate'] = -1
        fm.initial['enothi_id'] = request.user
        user_id = request.user
        mydata = Employee.objects.filter(enothi_id=request.user).values()
        if mydata.exists():
            print("mydata exists!!")
            print(request.POST)
            fm.initial['name'] = mydata[0]['ename']
            fm.initial['email'] = mydata[0]['eemail']
            fm.initial['empid'] = mydata[0]['empid']
            fm.initial['designation'] = mydata[0]['edesignation']
            fm.initial['division'] = mydata[0]['edivision']
           
            designations = Designation.objects.all()
            
            context = {
                'myProfileData': mydata[0],

                }
            #return HttpResponse(template.render(context, request))
            print("This is my data",mydata[0]['ename'])
            print("This is Employee Enothi ",fm['enothi_id'])
            return render(request,'employees/profile3.html',context)
        
    
    
    context = {
                'form':fm,
                'enothi_id':user_id,
                'employees_data': employees_data,
            }
    return render(request,'employees/profile.html',context)

@login_required(login_url='login')
def select_evaluatee(request):
    evaluator_empid = Employee.objects.filter(Q(enothi_id = request.user)).values('empid')[0]['empid']
    #preevaluatees = Evaluation.objects.filter(Q(evaluatorid = int(request.user.username))).values('evaluateeid')
    preevaluatees = Evaluation.objects.filter(Q(evaluatorid = evaluator_empid)).values('evaluateeid')
    #preevaluatee_ids = [item['evaluateeid'] for item in preevaluatees]

    if request.method == 'POST':
      
        print(int(request.user.username))
        if 'designations' in request.POST:
            selected_designations = request.POST.getlist('designations')
            print(selected_designations)
            print(request.user)
            evaluator_empid = Employee.objects.filter(Q(enothi_id = request.user)).values('empid')[0]['empid']
            print("Evaluator employee id",evaluator_empid)
            employees = Employee.objects.filter(Q(edesignation__in=selected_designations), ~Q(empid = evaluator_empid),  ~Q(empid__in=preevaluatees) ).values('empid', 'ename','enothi_id')
            
            employee_list = list(employees)
            return JsonResponse(employee_list, safe=False)
        elif 'employee' in request.POST: # Go for evaluation

            print("no designation here")
            print(request.POST['employee'][0:5])
            evaluatee_empid = int(request.POST['employee'][0:5])
            evaluator_empid = Employee.objects.filter(Q(enothi_id = request.user)).values('empid')[0]['empid']
            evaluatee = Employee.objects.filter(empid = evaluatee_empid).values()
            context = {
                'evaluateeData': evaluatee,
                }
            return redirect('evaluate',emp_id = evaluatee_empid)
        else: # without selecting designations
            
            evaluator_empid = Employee.objects.filter(Q(enothi_id = request.user)).values('empid')[0]['empid']
            employees = Employee.objects.filter(~Q(empid = evaluator_empid), ~Q(empid__in=preevaluatees)).values('empid', 'ename','enothi_id')
            employee_list = list(employees)
            #return JsonResponse(employee_list, safe=False)
            return redirect('select-evaluatee')
           
    
    else:
        evaluator_empid = Employee.objects.filter(Q(enothi_id = request.user)).values('empid')[0]['empid']
        print("this is working now!!")
        employees = Employee.objects.filter(~Q(empid = evaluator_empid),  ~Q(empid__in=preevaluatees)).values('empid', 'ename','enothi_id')
        #employees = Employee.objects.all()
        context = {
            'employeeData': employees
        }
        return render(request, 'employees/select_evaluatee.html', context)


@login_required(login_url='login')
def evaluate(request, emp_id):
    if request.method == 'POST':
        print("Evaluate Post Method ",request.user)
        for key, value in request.POST.items():
            print('Key: %s' % (key) ) 
            # print(f'Key: {key}') in Python >= 3.7
            print('Value %s' % (value) )
            # print(f'Value: {value}') in Python >= 3.7
        #print(request.GET['employee'][1:5]) # need to check
        print("Data type check ",type(request.user.id))
        print("Data type check ",(request.user))
        evaluateeid = int(request.POST['evaluateeid'])
        
        if 'secDept' in request.POST:
            secDeptEv = int(request.POST['secDept'])
        else:
            secDeptEv = 5

        if 'committee' in request.POST:
            commEv = int(request.POST['committee'])
        else:
            commEv = 5


        evaluatorid =  Employee.objects.filter(enothi_id = int(request.user.username)).values()[0]['empid']
        behavEv = int(request.POST['behaviour'])
        comid = 1 # need to be modified
        new_eval = Evaluation(evaluateeid = evaluateeid, evaluatorid = evaluatorid , secDeptEv = secDeptEv, commEv = commEv, behavEv = behavEv, comid = comid)
        #print(fm.cleaned_data)
        new_eval.save()
        return redirect('home')
    evaluatee_empid = emp_id #employee id must be of 4 digits
    evaluatee = Employee.objects.filter(empid = evaluatee_empid).values()[0]
    print("Evaluate function")
    print(evaluatee)
       
    context = {
                'evaluateeData': evaluatee,
                'evaluateeDesignation' : evaluatee['edesignation']
                }
    print("test ",context['evaluateeData']['ename'])
    return render(request,'employees/evaluate.html',context)
        #return render(request,'employees/evaluate.html') 

@login_required(login_url='login')
def showReport(request):

    if request.method == 'POST':
        print("Report Post method called")
        print(request.POST)
        if request.POST['profile'] == "Back to Query":
            designations = Designation.objects.all()
            employees = Employee.objects.all()
            context = {
                'designationData': designations,
                'employeeData': employees
            }
            return render(request,'employees/query.html',context)
        
        elif request.POST['evalBased'] == "everyone" :
            #print("Everyone's Evaluation ",)
            #print(request.POST['employee'])
            #print(int(request.POST['employee'][1:5]))
            #print(int(request.POST['employee'][0:5]))
            #evaluatee_section = Employee.objects.filter(empid = int(request.POST['employee'][1:5])).values()[0]['esection']
            all_evals = Evaluation.objects.filter(evaluateeid = int(request.POST['employee'])).values()
            results = []
            evaluatee_name = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['ename']
            evaluatee_designation = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['edesignation']
            evaluatee_division = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['edivision']
            #print(evaluatee_info)
            #print(type(all_evals))
            #print("Evaluatee Section : ",evaluatee_section)

            
            for eval in all_evals:
                results.append(eval)
                print("Evaluator ID : ",eval['evaluatorid'])
                print(type(eval['evaluatorid']))
                #evaluator_section = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]['esection']
               
            final_report = []
            #print(results)
            print("check eval")
            for eval in results:
                #print(eval['evaluatorid'])
                #print(Employee.objects.filter(empid = eval['evaluatorid']).values())
                evaluator = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]
                print("Evaluator Info : ",evaluator['ename'])
                print("Section : ",petro.sections[int(evaluator['esection'])-1][1])
                print("SecDept Eval : ",petro.remarks[int(eval['secDeptEv'])-1][1])
                print("Committee Eval : ",petro.remarks[int(eval['commEv'])-1][1])
                print("Behavior Eval : ",petro.remarks[int(eval['behavEv'])-1][1])

                final_report.append({
                                  'evaluatee': Employee.objects.filter(empid = eval['evaluateeid']).values()[0]['ename'],
                                  'evaluator': evaluator['ename'], 
                                  'division': evaluator['edivision'],
                                  'secDeptEval' : petro.remarks[int(eval['secDeptEv'])-1][1],
                                  'comEval' : petro.remarks[int(eval['commEv'])-1][1],
                                  'behavEval': petro.remarks[int(eval['behavEv'])-1][1],
                                    }
                                  )
            print("final Report")
            print(final_report)


            divisional_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            committee_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            behav_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            all_cat = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }

            for eval in final_report:
                #print(eval['secDeptEval'])
                if eval['secDeptEval'] != 'No Observation':
                    if eval['secDeptEval'] in divisional_work:
                        divisional_work[eval['secDeptEval']] += 1
                    else:
                        divisional_work[eval['secDeptEval']] += 1

            labels1 = list(divisional_work.keys())
            data1 = list(divisional_work.values())

            labels_json1 = json.dumps(labels1)
            data_json1 = json.dumps(data1)


            for eval in final_report:
                #print(eval['comEval'])
                if eval['comEval'] != 'No Observation':
                    if eval['comEval'] in committee_work:
                        committee_work[eval['comEval']] += 1
                    else:
                        committee_work[eval['comEval']] += 1

            print("Committee Work!!!!")
            #divisional_work['Good'] = 6
            print(committee_work)

            labels2 = list(committee_work.keys())
            data2 = list(committee_work.values())

            labels_json2 = json.dumps(labels2)
            data_json2 = json.dumps(data2)


            for eval in final_report:
                #print(eval['secDeptEval'])
                if eval['behavEval'] != 'No Observation':
                    if eval['behavEval'] in  behav_work:
                        behav_work[eval['behavEval']] += 1
                    else:
                        behav_work[eval['behavEval']] += 1

            labels3 = list(behav_work.keys())
            data3 = list(behav_work.values())

            labels_json3 = json.dumps(labels3)
            data_json3 = json.dumps(data3)


            all_cat['Excellent'] += divisional_work['Excellent'] + committee_work['Excellent'] + behav_work['Excellent']
            all_cat['Very Good'] += divisional_work['Very Good'] + committee_work['Very Good'] + behav_work['Very Good']
            all_cat['Good'] += divisional_work['Good'] + committee_work['Good'] + behav_work['Good']
            all_cat['Average'] += divisional_work['Average'] + committee_work['Average'] + behav_work['Average']

            labels4 = list(all_cat.keys())
            data4 = list(all_cat.values())

            labels_json4 = json.dumps(labels4)
            data_json4 = json.dumps(data4)

    
            context = {
                'evaluatee_name' :  evaluatee_name,
                'evaluatee_designation' : evaluatee_designation,
                'evaluatee_division' : evaluatee_division,
                'report_data': final_report,
                'labels_json1': labels_json1,
                'data_json1': data_json1,
                'labels_json2': labels_json2,
                'data_json2': data_json2,
                'labels_json3': labels_json3,
                'data_json3': data_json3,
                'labels_json4': labels_json4,
                'data_json4': data_json4,
                }
            



            return render(request,'employees/report.html',context)
        elif request.POST['evalBased'] == "secDept":
            print("Section or Department's evaluation")
            #print(type(int(request.POST['employee'][1:5])))
            #evaluatee_section = Employee.objects.filter(empid = int(request.POST['employee'][1:5])).values()[0]['esection']
            all_evals = Evaluation.objects.filter(evaluateeid = int(request.POST['employee'])).values()
            results = []
            evaluatee_name = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['ename']
            evaluatee_designation = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['edesignation']
            evaluatee_division = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['edivision']
            print(type(all_evals))
            #print("Evaluatee Section : ",evaluatee_section)

            
            for eval in all_evals:
                print("Evaluator ID : ",eval['evaluatorid'])
                print(type(eval['evaluatorid']))
                evaluator_division = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]['edivision']
                if evaluatee_division == evaluator_division:
                    print("Matched!! This should be inserted")
                    results.append(eval)
                #print("Evaluator Section : " ,query_set[0]['esection'])
                
                #results.append(eval)
            final_report = []
            print(results)
            for eval in results:
                evaluator = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]
                print("Evaluator Info : ",evaluator['ename'])
                print("Evaluator's division : ",evaluator['edivision'])
                print("Section : ",petro.sections[int(evaluator['esection'])-1][1])
                print("SecDept Eval : ",petro.remarks[int(eval['secDeptEv'])-1][1])
                print("Committee Eval : ",petro.remarks[int(eval['commEv'])-1][1])
                print("Behavior Eval : ",petro.remarks[int(eval['behavEv'])-1][1])

                final_report.append({
                                  'evaluatee': Employee.objects.filter(empid = eval['evaluateeid']).values()[0]['ename'],
                                  'evaluator': evaluator['ename'], 
                                  'division': evaluator['edivision'],
                                  'secDeptEval' : petro.remarks[int(eval['secDeptEv'])-1][1],
                                  'comEval' : petro.remarks[int(eval['commEv'])-1][1],
                                  'behavEval': petro.remarks[int(eval['behavEv'])-1][1],
                                    }
                                  )
            print("final Report")
            print(final_report)



            divisional_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            committee_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            behav_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            all_cat = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }

            for eval in final_report:
                #print(eval['secDeptEval'])
                if eval['secDeptEval'] in divisional_work:
                    divisional_work[eval['secDeptEval']] += 1
                else:
                    divisional_work[eval['secDeptEval']] += 1

            labels1 = list(divisional_work.keys())
            data1 = list(divisional_work.values())

            labels_json1 = json.dumps(labels1)
            data_json1 = json.dumps(data1)


            for eval in final_report:
                #print(eval['comEval'])
                if eval['comEval'] in committee_work:
                    committee_work[eval['comEval']] += 1
                else:
                    committee_work[eval['comEval']] += 1

            print("Committee Work!!!!")
            #divisional_work['Good'] = 6
            print(committee_work)

            labels2 = list(committee_work.keys())
            data2 = list(committee_work.values())

            labels_json2 = json.dumps(labels2)
            data_json2 = json.dumps(data2)


            for eval in final_report:
                #print(eval['secDeptEval'])
                if eval['behavEval'] in  behav_work:
                    behav_work[eval['behavEval']] += 1
                else:
                    behav_work[eval['behavEval']] += 1

            labels3 = list(behav_work.keys())
            data3 = list(behav_work.values())

            labels_json3 = json.dumps(labels3)
            data_json3 = json.dumps(data3)


            all_cat['Excellent'] += divisional_work['Excellent'] + committee_work['Excellent'] + behav_work['Excellent']
            all_cat['Very Good'] += divisional_work['Very Good'] + committee_work['Very Good'] + behav_work['Very Good']
            all_cat['Good'] += divisional_work['Good'] + committee_work['Good'] + behav_work['Good']
            all_cat['Average'] += divisional_work['Average'] + committee_work['Average'] + behav_work['Average']

            labels4 = list(all_cat.keys())
            data4 = list(all_cat.values())

            labels_json4 = json.dumps(labels4)
            data_json4 = json.dumps(data4)





            context = {
                'evaluatee_name' :  evaluatee_name,
                'evaluatee_designation' : evaluatee_designation,
                'evaluatee_division' : evaluatee_division,
                'report_data': final_report,
                'labels_json1': labels_json1,
                'data_json1': data_json1,
                'labels_json2': labels_json2,
                'data_json2': data_json2,
                'labels_json3': labels_json3,
                'data_json3': data_json3,
                'labels_json4': labels_json4,
                'data_json4': data_json4,
                }
            
            return render(request,'employees/report.html',context)
        elif request.POST['evalBased'] == "other":
            print("Other  Divisions Evaluation")
            #print(type(int(request.POST['employee'][1:5])))
            #evaluatee_section = Employee.objects.filter(empid = int(request.POST['employee'][1:5])).values()[0]['esection']
            all_evals = Evaluation.objects.filter(evaluateeid = int(request.POST['employee'])).values()
            results = []
            evaluatee_name = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['ename']
            evaluatee_designation = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['edesignation']
            evaluatee_division = Employee.objects.filter(empid = int(request.POST['employee'])).values()[0]['edivision']
            print(type(all_evals))
            #print("Evaluatee Section : ",evaluatee_section)

            
            for eval in all_evals:
                print("Evaluator ID : ",eval['evaluatorid'])
                print(type(eval['evaluatorid']))
                evaluator_division = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]['edivision']
                if evaluatee_division != evaluator_division:
                    print("UnMatched!! This should be inserted")
                    results.append(eval)
                #print("Evaluator Section : " ,query_set[0]['esection'])
                
                #results.append(eval)
            final_report = []
            print(results)
            for eval in results:
                evaluator = Employee.objects.filter(empid = eval['evaluatorid']).values()[0]
                print("Evaluator Info : ",evaluator['ename'])
                print("Evaluator's division : ",evaluator['edivision'])
                print("Section : ",petro.sections[int(evaluator['esection'])-1][1])
                print("SecDept Eval : ",petro.remarks[int(eval['secDeptEv'])-1][1])
                print("Committee Eval : ",petro.remarks[int(eval['commEv'])-1][1])
                print("Behavior Eval : ",petro.remarks[int(eval['behavEv'])-1][1])

                final_report.append({
                                  'evaluatee': Employee.objects.filter(empid = eval['evaluateeid']).values()[0]['ename'],
                                  'evaluator': evaluator['ename'], 
                                  'division': evaluator['edivision'],
                                  'secDeptEval' : petro.remarks[int(eval['secDeptEv'])-1][1],
                                  'comEval' : petro.remarks[int(eval['commEv'])-1][1],
                                  'behavEval': petro.remarks[int(eval['behavEv'])-1][1],
                                    }
                                  )
            print("final Report")
            print(final_report)



            divisional_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            committee_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            behav_work = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }
            all_cat = {
                    'Excellent':0, 'Very Good':0, 'Good':0, 'Average':0
            }

            for eval in final_report:
                #print(eval['secDeptEval'])
                if eval['secDeptEval'] in divisional_work:
                    divisional_work[eval['secDeptEval']] += 1
                else:
                    divisional_work[eval['secDeptEval']] += 1

            labels1 = list(divisional_work.keys())
            data1 = list(divisional_work.values())

            labels_json1 = json.dumps(labels1)
            data_json1 = json.dumps(data1)


            for eval in final_report:
                #print(eval['comEval'])
                if eval['comEval'] in committee_work:
                    committee_work[eval['comEval']] += 1
                else:
                    committee_work[eval['comEval']] += 1

            print("Committee Work!!!!")
            #divisional_work['Good'] = 6
            print(committee_work)

            labels2 = list(committee_work.keys())
            data2 = list(committee_work.values())

            labels_json2 = json.dumps(labels2)
            data_json2 = json.dumps(data2)


            for eval in final_report:
                #print(eval['secDeptEval'])
                if eval['behavEval'] in  behav_work:
                    behav_work[eval['behavEval']] += 1
                else:
                    behav_work[eval['behavEval']] += 1

            labels3 = list(behav_work.keys())
            data3 = list(behav_work.values())

            labels_json3 = json.dumps(labels3)
            data_json3 = json.dumps(data3)


            all_cat['Excellent'] += divisional_work['Excellent'] + committee_work['Excellent'] + behav_work['Excellent']
            all_cat['Very Good'] += divisional_work['Very Good'] + committee_work['Very Good'] + behav_work['Very Good']
            all_cat['Good'] += divisional_work['Good'] + committee_work['Good'] + behav_work['Good']
            all_cat['Average'] += divisional_work['Average'] + committee_work['Average'] + behav_work['Average']

            labels4 = list(all_cat.keys())
            data4 = list(all_cat.values())

            labels_json4 = json.dumps(labels4)
            data_json4 = json.dumps(data4)





            context = {
                'evaluatee_name' :  evaluatee_name,
                'evaluatee_designation' : evaluatee_designation,
                'evaluatee_division' : evaluatee_division,
                'report_data': final_report,
                'labels_json1': labels_json1,
                'data_json1': data_json1,
                'labels_json2': labels_json2,
                'data_json2': data_json2,
                'labels_json3': labels_json3,
                'data_json3': data_json3,
                'labels_json4': labels_json4,
                'data_json4': data_json4,
                }
            
            return render(request,'employees/report.html',context)
        
        
        
        
        context = {
                'report_data': final_report,
                }
        return render(request,'employees/report.html',context)
    
    designations = Designation.objects.all()
    employees = Employee.objects.all()
    context = {
                'designationData': designations,
                'employeeData': employees
            }
    return render(request,'employees/query.html',context)


@login_required(login_url='login')
def giveAward(request):
    if request.method == 'POST':

        print("checkkk!!!!!!!")
        print(request.POST['employee'])
        print(request.POST['permission'])
        return redirect('home')
        #return redirect('writeAwardDescription',emp_id = int(request.POST['employee']))
    employee = Employee.objects.all()
    return render (request, 'employees/award.html', {'employeeData': employee} )
    

@login_required(login_url='login')
def writeAwardDescription(request,emp_id):
    if request.method == 'POST':
        #print(request.POST['giveAward'])
        #print(request.POST['employee'])
        print("if from writeAwardDescription")
        
    print("get from write award")
    employee = Employee.objects.all()
    return render (request, 'employees/write_award_description.html', {'employeeData': employee} )


@login_required(login_url='login')
def get_employee_data(request):

    #print(cwd)
    df = pd.read_excel("employees.xlsx")
    employees_data = df.to_dict(orient='records')
    #print(df.loc[[0]])
    print(employees_data[0])
    if request.method == 'GET' and 'employee_name' in request.GET:
        employee_name = request.GET.get('employee_name')
        print("this is running as well")
        #print(employee_name)
        for employee in employees_data:
            idname = "["+str(employee['ID'])+"] - "+employee['Name']
            
            if idname == employee_name:
                print("got in list")
                print(idname)
                data = {
                    'name':employee['Name'],
                    'designation': employee['Designation'],
                    'division': employee['Department'],
                    'empid' : employee['ID']
                }
    
                return JsonResponse(data)
    fm = NewEmployeeRegistration()
    context = {
                'form':fm,
                'employees_data': employees_data,
                }
    return render (request, 'employees/testProfile.html',context)



@login_required(login_url='login')
def pie_chart(request):
    # Example: Querying data for pie chart
    employees = Employee.objects.all()
    designation_counts = {
        'aa':5,'bb':6,'cc':8,'dd':10
    }
    
    #for emp in employees:
    #    if emp.edesignation in designation_counts:
    #        designation_counts[emp.edesignation] += 1
    #    else:
    #        designation_counts[emp.edesignation] = 1
    
    # Prepare data for Chart.js

    labels = list(designation_counts.keys())
    data = list(designation_counts.values())

    labels_json = json.dumps(labels)
    data_json = json.dumps(data)
    
    context = {
        'labels_json': labels_json,
        'data_json': data_json,
    }
    print(designation_counts)
    return render(request, 'employees/piechart.html', context)