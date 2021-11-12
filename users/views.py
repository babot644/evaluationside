from datetime import time
import datetime
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
    try:
        user_signin = auth.sign_in_with_email_and_password(loginUsername, loginPassword)
    except:
        messages.warning(request, "Incorrect email or Password" )
        return render(request,  'users/login.html') 
    for avail in seminars:
        value = avail.to_dict()
        availSeminars.append(value)
    request.session['userSession'] = user_signin['email']
    
    userSession = request.session['userSession']
    return render(request,  'evaluation/availableseminars.html', {"Username":userSession, "available":availSeminars})
def registerUser(request):
        registerAddress = request.POST.get('registerAddress')
        registerEmail = request.POST.get("registerEmail")
        registerPassword = request.POST.get("registerPassword")
        registerCPassword = request.POST.get('registerCPassword')
        registerFirstName = request.POST.get('registerFirstName')
        registerMiddleName = request.POST.get('registerMiddleName')
        registerLastName = request.POST.get('registerLastName')
        registerContactNumber = request.POST.get('registerContactNumber')
        now = int(time.time())
        registerGender = request.POST.get('gender')
        data = {
            u'address': registerAddress,
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
                    return render(request,  'users/login.html')
        elif len(registerPassword) > 25 and len(registerCPassword) > 25:
                    messages.warning(request, "Please make your password stronger 8 characters minimum 25 maximum")
                    return render(request,  'users/login.html')

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
    seminars = firestoreDB.collection(u'seminars').get()
    availSeminars = []
    if request.session['userSession']:
        userLoggedin = request.session['userSession']
        for avail in seminars:
            value = avail.to_dict()
            availSeminars.append(value)
        return render(request,  'evaluation/availableseminars.html', {"Username":userLoggedin, "available":availSeminars})
    else:
        return render(request,  'users/login.html') 

    
def evaluateSeminar(request):
    seminarTitle = request.POST.get("seminarTitle")
    seminarDatePosted = request.POST.get("date_posted")
    seminarFacilitator = request.POST.get("seminarFacilitator")
    seminar_id = request.POST.get("seminar_id")
    seminarInfo = {
        "seminar_id": seminar_id,
        "Title": seminarTitle,
        "date_posted": seminarDatePosted,
        "Facilitator": seminarFacilitator,
    }
    if request.session['userSession']:
        userLoggedin = request.session['userSession']
    return render(request, 'evaluation/evaluate.html', {"Username": userLoggedin,"seminarInfo": seminarInfo})

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
        
        x = firestoreDB.collection(u'evaluations').document(seminar_id).collection("evaluators").document(yawa[0]['evaluator_id'])
        x.set(data)
        messages.success(request, "Thankyou for your evaluation!." )
        return render(request,  'evaluation/availableseminars.html', {"Username": userLoggedin})  
    else:
        if request.session['userSession']:
            userLoggedin = request.session['userSession']
        messages.warning(request, "Please rate all questions.." )
        return render(request,  'evaluation/availableseminars.html', {"Username": userLoggedin})  

    