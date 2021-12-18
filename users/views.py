from datetime import time
import datetime
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages
import requests
import time
import pyrebase
import requests, json


# Create your views here.


config = {
  "apiKey": "AIzaSyCRm30U4IA0BFi85g_5qfjF8QB4hF_iuqU",
  "authDomain": "evaluation-system-690d2.firebaseapp.com",
  "databaseURL": "https://evaluation-system-690d2-default-rtdb.firebaseio.com",
  "projectId": "evaluation-system-690d2",
  "storageBucket": "evaluation-system-690d2.appspot.com",
  "messagingSenderId": "69328407149",
  "appId": "1:69328407149:web:c7b6326bf6d40a67140d64",
  "measurementId": "G-687GYC9DLD"
}

firebase=pyrebase.initialize_app(config)
cred = credentials.Certificate("users/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firestoreDB = firestore.client()
auth = firebase.auth()
database=firebase.database()



def forgotPassword(request):
    return render(request, 'users/forgotpassword.html')
def forgotPasswordConfirm(request):
    forgotEmail = request.POST.get('forgotPasswordConfirm')
    try:
        auth.send_password_reset_email(forgotEmail)
        messages.success(request, "Please check your email to reset your password" )
    except:
        messages.warning(request, "Incorrect email or Password" )
        return render(request, 'users/forgotpassword.html')
    
    return render(request, 'users/forgotpassword.html')

def login(request):
    userLogged = request.session['logged_in_user']
    if userLogged:
        return render(request,  'evaluation/availableseminars.html')
    else:
        return render(request, 'users/login.html') 

def loginUser(request):
    loginUsername = request.POST.get("loginUsername")
    loginPassword = request.POST.get("loginPassword")
    evaluator = firestoreDB.collection(u'evaluators').get()
    seminars = firestoreDB.collection(u'seminars').get()
    
    availSeminars = []
    seminarFacilitators = []
    facilitatorcounts = []
    facilitato = {}
    
    
    try:
        user_signin = auth.sign_in_with_email_and_password(loginUsername, loginPassword)
    except:
        messages.warning(request, "Incorrect email or Password" )
        return render(request,  'users/login.html') 
    for avail in seminars:
        facilitatorcount = 0
        
        value = avail.to_dict()
        
        availSeminars.append(value)
        val = value['seminar_id']
        facilitators = firestoreDB.collection(u'seminars').document(str(val)).collection("facilitators").get()
        for x in facilitators:
            facilitators = {}
            facilitatorcount = facilitatorcount+1
            yawa = "facilitator" + str(facilitatorcount)
            valyu = x.to_dict() 
            facilitators = {yawa: valyu['facilitator_name']}
            value[yawa] = valyu['facilitator_name']
        value['facilicount'] = facilitatorcount
    


    
    


   # for i in availSeminars:
   #     y = 0
   #     facilitatorcount = 0
   #     val = i['seminar_id']
   #     facilitators = firestoreDB.collection(u'seminars').document(str(val)).collection("facilitators").get()
   #     for x in facilitators:
   #         facilitatorcount = facilitatorcount+1
   #         valyu = x.to_dict() 
   #         seminarFacilitators.append(valyu['facilitator_name'])
   #             
   # facilitatorcounts.append(facilitatorcount)
   # y = y+1
             
        
                 
    request.session['userSession'] = user_signin['email']
    
    userSession = request.session['userSession']
    return render(request,  'evaluation/availableseminars.html', {"Username":userSession, "available":availSeminars, "facilitators":seminarFacilitators, "facilitatorcount":facilitatorcounts})
def registerUser(request):
        registerAddress = request.POST.get('registerAddress')
        registerEmail = request.POST.get("registerEmail")
        registerPassword = request.POST.get("registerPassword")
        registerCPassword = request.POST.get('registerCPassword')
        registerFirstName = request.POST.get('registerFirstName')
        registerMiddleName = request.POST.get('registerMiddleName')
        registerLastName = request.POST.get('registerLastName')
        registerContactNumber = request.POST.get('registerContactNumber')
        registerPosition = request.POST.get('registerPosition')
        now = int(time.time())
        registerGender = request.POST.get('gender')
        data = {
            u'position': registerPosition,
            u'school_office': registerAddress,
            u'gender': registerGender,
            u'email': registerEmail,
            u'password': registerPassword,
            u'first_name': registerFirstName,
            u'middle_name': registerMiddleName,
            u'last_name': registerLastName,
            u'phone_number': registerContactNumber,
            u'evaluator_id': str(now),
            u'date_created': datetime.datetime.now(),
            }
        if len(registerPassword) < 8 and len(registerCPassword) < 8:
                    messages.warning(request, "Please make your password stronger 8 characters minimum 25 maximum")
                    
        elif len(registerPassword) > 25 and len(registerCPassword) > 25:
                    messages.warning(request, "Please make your password stronger 8 characters minimum 25 maximum")
                    

        if registerPassword == registerCPassword:  
                try:
                        if registerEmail.find("@deped.gov.ph") < 1:
                            messages.warning(request, "Please use @deped.gov.ph email")
                            return render(request,  'users/login.html')
                        user = auth.create_user_with_email_and_password(registerEmail, registerPassword)
                        doc_ref = firestoreDB.collection(u'evaluators').document(str(now))
                        doc_ref2 = firestoreDB.collection(u'evaluator_report').document(str(now))
                        doc_ref2.set(data)
                        doc_ref.set(data)
                        messages.success(request, "New User Registered!" )
                        return render(request,  'users/login.html') 
                except:
                     messages.warning(request, "Email Already Taken")
                     return render(request, 'users/login.html')
        else:
            messages.warning(request, "Password Do not Match!")
            return render(request,  'users/login.html')
        
        
def availableSeminars(request):
    try:
        del request.session['facilitator1']
        del request.session['facilitator2']
        del request.session['facilitator3']
        del request.session['facilitator4']
        del request.session['seminar_id']
    except KeyError:
        pass
    seminars = firestoreDB.collection(u'seminars').get()
    availSeminars = []
    if request.session['userSession']:
        userLoggedin = request.session['userSession']
        for avail in seminars:
            facilitatorcount = 0
            value = avail.to_dict()
            availSeminars.append(value)
            val = value['seminar_id']
            facilitators = firestoreDB.collection(u'seminars').document(str(val)).collection("facilitators").get()
            for x in facilitators:
                facilitators = {}
                facilitatorcount = facilitatorcount+1
                yawa = "facilitator" + str(facilitatorcount)
                valyu = x.to_dict() 
                facilitators = {yawa: valyu['facilitator_name']}
                value[yawa] = valyu['facilitator_name']
            value['facilicount'] = facilitatorcount
        return render(request,  'evaluation/availableseminars.html', {"Username":userLoggedin, "available":availSeminars})
    else:
        return render(request,  'users/login.html') 

    
def evaluateSeminar(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    if(request.POST.get("seminarFacilitator1")):
        request.session['facilitator1'] = request.POST.get("seminarFacilitator1")
    if(request.POST.get("seminarFacilitator2")):
        request.session['facilitator2'] = request.POST.get("seminarFacilitator2")
    if(request.POST.get("seminarFacilitator3")):
        request.session['facilitator3'] = request.POST.get("seminarFacilitator3")
    if(request.POST.get("seminarFacilitator4")):
        request.session['facilitator4'] = request.POST.get("seminarFacilitator4")


    seminar_id = request.POST.get("seminar_id")
    request.session["seminar_id"] = seminar_id
    seminarInfo = {
        "seminar_id": seminar_id,
        "seminarTitle": seminarTitle,
        "date_posted": seminarDatePosted,
        
    }
    if request.session['userSession']:
        userLoggedin = request.session['userSession']
    return render(request, 'evaluation/evaluate.html', {"Username": userLoggedin,"seminarInfo": seminarInfo})


def firstEvaluation(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    back = request.POST.get("back")
    facilitators = {}
    if(request.POST.get("Facilitator1")):
        seminarFacilitator1 = request.POST.get("Facilitator1")
        facilitators["facilitator1"] = seminarFacilitator1
    if(request.POST.get("Facilitator2")):
        seminarFacilitator2 = request.POST.get("Facilitator2")
        facilitators["facilitator2"] = seminarFacilitator2
    if(request.POST.get("Facilitator3")):
        seminarFacilitator3 = request.POST.get("Facilitator3")
        facilitators["facilitator3"] = seminarFacilitator3
    if(request.POST.get("Facilitator4")):
        seminarFacilitator4 = request.POST.get("Facilitator4")
        facilitators["facilitator4"] = seminarFacilitator4
    
    q1 = request.POST.get("1q1")
    q2 = request.POST.get("1q2")
    q3 = request.POST.get("1q3")
    q4 = request.POST.get("1q4")
    q5 = request.POST.get("1q5")
    q6 = request.POST.get("1q6")
    q7 = request.POST.get("1q7")
    q8 = request.POST.get("1q8")
    seminar_id = request.POST.get("seminar_id")
    now = int(time.time())
    evaluatorEmail = str(request.session['userSession'])
    docs = firestoreDB.collection('evaluators').where('email', '==', evaluatorEmail).get()
    yawa = []
    for doc in docs:
        yawa.append(doc.to_dict())

    fullName = yawa[0]['first_name'] + " " + yawa[0]['middle_name'] + " " + yawa[0]['last_name']
    data = {
        "full_name": fullName,
        "date_evaluated": now,
        "evaluatorEmail": evaluatorEmail,
        "seminarTitle" : seminarTitle,
        "date_posted" : seminarDatePosted,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'q4': q4,
        'q5': q5,
        'q6': q6,
        'q7': q7,
        'q8': q8,
    }
    
    if back:
        return render(request,  'evaluation/evaluate.html', {"facilitato": facilitators, "data": data, "seminar_id": seminar_id })
    if q1 and q2 and q3 and q4 and q5 and q6 and q7 and q8:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        x = firestoreDB.collection('evaluations').document(request.session['seminar_id']).collection("evaluators").document(yawa[0]['evaluator_id'])
        x.set(data)
        for key, value in facilitators.items():
            x.collection("facilitators").document(value).set({key : value})
        return render(request,  'evaluation/evaluate2.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please evaluate all questions")
        return render(request,  'evaluation/evaluate.html', {"Username": userLoggedin, "facilitato": facilitators, "seminarInfo": data, "seminar_id": seminar_id })

def secondEvaluation(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    selectedFacilitator = request.POST.get("selectedFacilitator")
    facilitators = {}
    if(request.POST.get("facilitator1")):
        seminarFacilitator1 = request.POST.get("facilitator1")
        facilitators["facilitator1"] = seminarFacilitator1
    if(request.POST.get("facilitator2")):
        seminarFacilitator2 = request.POST.get("facilitator2")
        facilitators["facilitator2"] = seminarFacilitator2
    if(request.POST.get("facilitator3")):
        seminarFacilitator3 = request.POST.get("facilitator3")
        facilitators["facilitator3"] = seminarFacilitator3
    if(request.POST.get("facilitator4")):
        seminarFacilitator4 = request.POST.get("facilitator4")
        facilitators["facilitator4"] = seminarFacilitator4
    
    qq1 = request.POST.get("2q1")
    qq2 = request.POST.get("2q2")
    qq3 = request.POST.get("2q3")
    qq4 = request.POST.get("2q4")
    qq5 = request.POST.get("2q5")
    qq6 = request.POST.get("2q6")
    qq7 = request.POST.get("2q7")
    qq8 = request.POST.get("2q8")
    qq9 = request.POST.get("2q9")
    seminar_id = request.POST.get("seminar_id")
    now = int(time.time())
    evaluatorEmail = str(request.session['userSession'])
    docs = firestoreDB.collection('evaluators').where('email', '==', evaluatorEmail).get()
    yawa = []
    for doc in docs:
        yawa.append(doc.to_dict())

    fullName = yawa[0]['first_name'] + " " + yawa[0]['middle_name'] + " " + yawa[0]['last_name']
    data = {
        "full_name": fullName,
        "date_evaluated": now,
        "evaluatorEmail": evaluatorEmail,
        "seminarTitle" : seminarTitle,
        "date_posted" : seminarDatePosted,
        'q9': qq1,
        'q10': qq2,
        'q11': qq3,
        'q12': qq4,
        'q13': qq5,
        'q14': qq6,
        'q15': qq7,
        'q16': qq8,
        'q17': qq9,
    }
    data2 = {
        'q9': qq1,
        'q10': qq2,
        'q11': qq3,
        'q12': qq4,
        'q13': qq5,
        'q14': qq6,
        'q15': qq7,
        'q16': qq8,
        'q17': qq9,
    }
    back = request.POST.get("back")
    if back:
        return render(request,  'evaluation/evaluate2.html', {"facilitato": facilitators, "data": data, "seminar_id": seminar_id })
    if qq1 and qq2 and qq3 and qq4 and qq5 and qq6 and qq7 and qq8 and qq9 and selectedFacilitator:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
            x = firestoreDB.collection('evaluations').document(request.session['seminar_id']).collection("evaluators").document(yawa[0]['evaluator_id']).collection("facilitators").document(selectedFacilitator)
            x.update(data2)
            
        return render(request,  'evaluation/evaluate3.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please evaluate all questions")
        return render(request,  'evaluation/evaluate2.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })
     

def thirdEvaluation(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    facilitators = {}
    if(request.POST.get("facilitator1")):
        seminarFacilitator1 = request.POST.get("facilitator1")
        facilitators["facilitator1"] = seminarFacilitator1
    if(request.POST.get("facilitator2")):
        seminarFacilitator2 = request.POST.get("facilitator2")
        facilitators["facilitator2"] = seminarFacilitator2
    if(request.POST.get("facilitator3")):
        seminarFacilitator3 = request.POST.get("facilitator3")
        facilitators["facilitator3"] = seminarFacilitator3
    if(request.POST.get("facilitator4")):
        seminarFacilitator4 = request.POST.get("facilitator4")
        facilitators["facilitator4"] = seminarFacilitator4
    
    qqq1 = request.POST.get("3q1")
    qqq2 = request.POST.get("3q2")
    qqq3 = request.POST.get("3q3")
    
    seminar_id = request.POST.get("seminar_id")
    now = int(time.time())
    evaluatorEmail = str(request.session['userSession'])
    docs = firestoreDB.collection('evaluators').where('email', '==', evaluatorEmail).get()
    yawa = []
    for doc in docs:
        yawa.append(doc.to_dict())

    fullName = yawa[0]['first_name'] + " " + yawa[0]['middle_name'] + " " + yawa[0]['last_name']
    data = {
        "full_name": fullName,
        
        "evaluatorEmail": evaluatorEmail,
        "seminarTitle" : seminarTitle,
        "date_posted" : seminarDatePosted,
        'q18': qqq1,
        'q19': qqq2,
        'q20': qqq3,
        
    }
    back = request.POST.get("back")
    if back:
        return render(request,  'evaluation/evaluate3.html', {"facilitato": facilitators, "data": data, "seminar_id": seminar_id })
    if qqq1 and qqq2 and qqq3:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
            x = firestoreDB.collection('evaluations').document(request.session['seminar_id']).collection("evaluators").document(yawa[0]['evaluator_id'])
            x.update(data)
        return render(request,  'evaluation/evaluate4.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please evaluate all questions")
        return render(request,  'evaluation/evaluate3.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })
def fourthEvaluation(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    facilitators = {}
    if(request.POST.get("facilitator1")):
        seminarFacilitator1 = request.POST.get("facilitator1")
        facilitators["facilitator1"] = seminarFacilitator1
    if(request.POST.get("facilitator2")):
        seminarFacilitator2 = request.POST.get("facilitator2")
        facilitators["facilitator2"] = seminarFacilitator2
    if(request.POST.get("facilitator3")):
        seminarFacilitator3 = request.POST.get("facilitator3")
        facilitators["facilitator3"] = seminarFacilitator3
    if(request.POST.get("facilitator4")):
        seminarFacilitator4 = request.POST.get("facilitator4")
        facilitators["facilitator4"] = seminarFacilitator4
    
    qqqq1 = request.POST.get("4q1")
    qqqq2 = request.POST.get("4q2")
    qqqq3 = request.POST.get("4q3")
    
    seminar_id = request.POST.get("seminar_id")
    now = int(time.time())
    evaluatorEmail = str(request.session['userSession'])
    docs = firestoreDB.collection('evaluators').where('email', '==', evaluatorEmail).get()
    yawa = []
    for doc in docs:
        yawa.append(doc.to_dict())

    fullName = yawa[0]['first_name'] + " " + yawa[0]['middle_name'] + " " + yawa[0]['last_name']
    data = {
        "full_name": fullName,
        
        "evaluatorEmail": evaluatorEmail,
        "seminarTitle" : seminarTitle,
        "date_posted" : seminarDatePosted,
        'q21': qqqq1,
        'q22': qqqq2,
        'q23': qqqq3,
    }
    back = request.POST.get("back")
    if back:
        return render(request,  'evaluation/evaluate4.html', {"facilitato": facilitators, "data": data, "seminar_id": seminar_id })
    if qqqq1 and qqqq2 and qqqq3:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
            x = firestoreDB.collection('evaluations').document(request.session['seminar_id']).collection("evaluators").document(yawa[0]['evaluator_id'])
            x.update(data)
        return render(request,  'evaluation/evaluate5.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please evaluate all questions")
        return render(request,  'evaluation/evaluate5.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })

def fifthEvaluation(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    facilitators = {}
    if(request.POST.get("facilitator1")):
        seminarFacilitator1 = request.POST.get("facilitator1")
        facilitators["facilitator1"] = seminarFacilitator1
    if(request.POST.get("facilitator2")):
        seminarFacilitator2 = request.POST.get("facilitator2")
        facilitators["facilitator2"] = seminarFacilitator2
    if(request.POST.get("facilitator3")):
        seminarFacilitator3 = request.POST.get("facilitator3")
        facilitators["facilitator3"] = seminarFacilitator3
    if(request.POST.get("facilitator4")):
        seminarFacilitator4 = request.POST.get("facilitator4")
        facilitators["facilitator4"] = seminarFacilitator4
    
    qqqqq1 = request.POST.get("5q1")
    qqqqq2 = request.POST.get("5q2")
    qqqqq3 = request.POST.get("5q3")
    qqqqq4 = request.POST.get("5q4")
    
    seminar_id = request.POST.get("seminar_id")
    now = int(time.time())
    evaluatorEmail = str(request.session['userSession'])
    docs = firestoreDB.collection('evaluators').where('email', '==', evaluatorEmail).get()
    yawa = []
    for doc in docs:
        yawa.append(doc.to_dict())

    fullName = yawa[0]['first_name'] + " " + yawa[0]['middle_name'] + " " + yawa[0]['last_name']
    data = {
        "full_name": fullName,
        
        "evaluatorEmail": evaluatorEmail,
        "seminarTitle" : seminarTitle,
        "date_posted" : seminarDatePosted,
        'q24': qqqqq1,
        'q25': qqqqq2,
        'q26': qqqqq3,
        'q27': qqqqq4,
    }
    back = request.POST.get("back")
    if back:
        return render(request,  'evaluation/evaluate5.html', {"facilitato": facilitators, "data": data, "seminar_id": seminar_id })
    if qqqqq1 and qqqqq2 and qqqqq3 and qqqqq4:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
            x = firestoreDB.collection('evaluations').document(request.session['seminar_id']).collection("evaluators").document(yawa[0]['evaluator_id'])
            x.update(data)
        return render(request,  'evaluation/evaluate6.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please evaluate all questions")
        return render(request,  'evaluation/evaluate5.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })

def sixthEvaluation(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    facilitators = {}
    if(request.POST.get("facilitator1")):
        seminarFacilitator1 = request.POST.get("facilitator1")
        facilitators["facilitator1"] = seminarFacilitator1
    if(request.POST.get("facilitator2")):
        seminarFacilitator2 = request.POST.get("facilitator2")
        facilitators["facilitator2"] = seminarFacilitator2
    if(request.POST.get("facilitator3")):
        seminarFacilitator3 = request.POST.get("facilitator3")
        facilitators["facilitator3"] = seminarFacilitator3
    if(request.POST.get("facilitator4")):
        seminarFacilitator4 = request.POST.get("facilitator4")
        facilitators["facilitator4"] = seminarFacilitator4
    
    qqqqqq1 = request.POST.get("6q1")
    qqqqqq2 = request.POST.get("6q2")
    qqqqqq3 = request.POST.get("6q3")
    qqqqqq4 = request.POST.get("6q4")
    
    seminar_id = request.POST.get("seminar_id")
    now = int(time.time())
    evaluatorEmail = str(request.session['userSession'])
    docs = firestoreDB.collection('evaluators').where('email', '==', evaluatorEmail).get()
    yawa = []
    for doc in docs:
        yawa.append(doc.to_dict())

    fullName = yawa[0]['first_name'] + " " + yawa[0]['middle_name'] + " " + yawa[0]['last_name']
    data = {
        "full_name": fullName,
        
        "evaluatorEmail": evaluatorEmail,
        "seminarTitle" : seminarTitle,
        "date_posted" : seminarDatePosted,
        'q28': qqqqqq1,
        'q29': qqqqqq2,
        'q30': qqqqqq3,
        'q31': qqqqqq4,
    }
    back = request.POST.get("back")
    if back:
        return render(request,  'evaluation/evaluate5.html', {"facilitato": facilitators, "data": data, "seminar_id": seminar_id })
    if qqqqqq1 and qqqqqq2 and qqqqqq3 and qqqqqq4:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
            x = firestoreDB.collection('evaluations').document(request.session['seminar_id']).collection("evaluators").document(yawa[0]['evaluator_id'])
            x.update(data)
        return render(request,  'evaluation/evaluate7.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please evaluate all questions")
        return render(request,  'evaluation/evaluate6.html', {"Username": userLoggedin, "facilitato": facilitators, "data": data, "seminar_id": seminar_id })


def evaluationInfo(request):
    q1 = request.POST.get("1q1")
    q2 = request.POST.get("1q2")
    q3 = request.POST.get("1q3")
    q4 = request.POST.get("1q4")
    q5 = request.POST.get("1q5")
    q6 = request.POST.get("1q6")
    q7 = request.POST.get("1q7")
    q8 = request.POST.get("1q8")
    qq1 = request.POST.get("2q1")
    qq2 = request.POST.get("2q2")
    qq3 = request.POST.get("2q3")
    qq4 = request.POST.get("2q4")
    qq5 = request.POST.get("2q5")
    qq6 = request.POST.get("2q6")
    qq7 = request.POST.get("2q7")
    qq8 = request.POST.get("2q8")
    qq9 = request.POST.get("2q9")
    qqq1 = request.POST.get("3q1")
    qqq2 = request.POST.get("3q2")
    qqq3 = request.POST.get("3q3")
    qqqq1 = request.POST.get("4q1")
    qqqq2 = request.POST.get("4q2")
    qqqq3 = request.POST.get("4q3")
    qqqqq1 = request.POST.get("5q1")
    qqqqq2 = request.POST.get("5q2")
    qqqqq3 = request.POST.get("5q3")
    qqqqq4 = request.POST.get("5q4")
    qqqqqq1 = request.POST.get("6q1")
    qqqqqq2 = request.POST.get("6q2")
    qqqqqq3 = request.POST.get("6q3")
    qqqqqq4 = request.POST.get("6q4")
    comment1 = request.POST.get("hiddenComment1")
    comment2 = request.POST.get("hiddenComment2")
    comment3 = request.POST.get("hiddenComment3")
    comment4 = request.POST.get("hiddenComment4")
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    seminarFacilitator = request.POST.get("Facilitator")
    seminar_id = request.POST.get("seminar_id")
    now = int(time.time())
    evaluatorEmail = str(request.session['userSession'])
    docs = firestoreDB.collection('evaluators').where('email', '==', evaluatorEmail).get()
    yawa = []
    for doc in docs:
        yawa.append(doc.to_dict())
    

    fullName = yawa[0]['first_name'] + " " + yawa[0]['middle_name'] + " " + yawa[0]['last_name']
    data = {
            "full_name": fullName,
            "date_evaluated": now,
            "evaluatorEmail": evaluatorEmail,
            "seminarTitle" : seminarTitle,
            "seminarDatePosted" : seminarDatePosted,
            "seminarFacilitator" : seminarFacilitator,
            'q1': q1,
            'q2': q2,
            'q3': q3,
            'q4': q4,
            'q5': q5,
            'q6': q6,
            'q7': q7,
            'q8': q8,
            'q9': qq1,
            'q10': qq2,
            'q11': qq3,
            'q12': qq4,
            'q13': qq5,
            'q14': qq6,
            'q15': qq7,
            'q16': qq8,
            'q17': qq9,
            'q18': qqq1,
            'q19': qqq2,
            'q20': qqq3,
            'q21': qqqq1,
            'q22': qqqq2,
            'q23': qqqq3,
            'q24': qqqqq1,
            'q25': qqqqq2,
            'q26': qqqqq3,
            'q27': qqqqq4,
            'q28': qqqqqq1,
            'q29': qqqqqq2,
            'q30': qqqqqq3,
            'q31': qqqqqq4,
            'comment1': comment1,
            'comment2': comment2,
            'comment3': comment3,
            'comment4': comment4,
            }
    data2 = {
        'evaluated': True,
    }
    
    if q1 and q2 and q3 and q4 and q5 and q6 and q7 and q8 and qq1 and qq2 and qq3 and qq4 and qq5 and qq6 and qq7 and qq8 and qq9 and qqq1 and qqq2 and qqq3 and qqqq1 and qqqq2 and qqqq3 and qqqqq1 and qqqqq2 and qqqqq3 and qqqqq4 and qqqqqq1 and qqqqqq2 and qqqqqq3 and qqqqqq4 and comment1 and comment2 and comment3 and comment4 :
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        
        x = firestoreDB.collection('evaluations').document(seminar_id).collection("evaluators").document(yawa[0]['evaluator_id'])
        x.add(data)
        messages.success(request, "Thankyou for your evaluation!." )
        return render(request,  'evaluation/availableseminars.html', {"Username": userLoggedin})  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please rate all questions.." )
        return render(request,  'evaluation/availableseminars.html', {"Username": userLoggedin})  


def logout(request):
    
    try:
        del request.session['facilitator1']
        del request.session['facilitator2']
        del request.session['facilitator3']
        del request.session['facilitator4']
        del request.session['seminar_id']
    except KeyError:
        pass
    
    return render(request, 'users/logout.html')
    
