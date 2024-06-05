from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
import random
from django.contrib.auth import logout
import pickle
import os
from django.http import HttpResponseNotFound

from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

import urllib.request
import urllib.parse


def sendSMS(user,otp,mobile):
    data =  urllib.parse.urlencode({'username':'Codebook','apikey': '56dbbdc9cea86b276f6c' , 'mobile': mobile,
        'message' : f'Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you', 'senderid': 'CODEBK'})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data)
    return f.read()
 








def index(request):
    return render(request,'user/index.html')



def about(request):
    return render(request,'user/about.html')



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('admin_login')
    return render(request,'user/admin-login.html')



def contact(request):
    return render(request,'user/contact.html')









def services(request):
    return render(request,'user/service.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(user_email=email)   
            if user.user_password == password:
                request.session['user_id'] = user.user_id
                if user.status == 'Accepted':
                    messages.success(request, 'Login Successful')
                    return redirect('user_dashboard')
                elif user.status == 'Pending':
                    resp = sendSMS(user.user_name, user.otp, user.user_phone)
                    messages.info(request, 'Otp verification is compalsary otp is sent to ' + str(user.user_phone))
                    return redirect('otp')
                else:
                    messages.error(request, 'Your account is not approved yet.')
                    return redirect('user_login')
            else:
                messages.error(request, 'Incorrect Password')
                return redirect('user_login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid Login Details')
            return redirect('user_login')
    return render(request,'user/user-login.html')


def user_dashboard(request):
    return render(request,'user/user-dashboard.html')


def user_profile(request):
    user_id  = request.session['user_id']
    print(user_id)
    user = User.objects.get(pk= user_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            user.user_profile = profile
        except MultiValueDictKeyError:
            profile = user.user_profile
        password = request.POST.get('password')
        location = request.POST.get('location')
        user.user_name = name
        user.user_email = email
        user.user_phone = phone
        user.user_password = password
        user.user_location = location
        user.save()
        messages.success(request , 'updated succesfully!')
        return redirect('user_profile')
    return render(request,'user/user-profile.html',{'user':user})





def generate_otp(length=4):
    otp = ''.join(random.choices('0123456789', k=length))
    return otp




def user_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        location = request.POST.get('address')
        profile = request.FILES.get('profile')
        try:
            User.objects.get(user_email =   email)
            messages.info(request, 'Email Already Exists!')
            return redirect('user_register')
        except:
            otp = generate_otp()
            user = User.objects.create(user_name=name, user_email=email, user_phone=phone, user_profile=profile, user_password=password, user_location=location,otp=otp)
            print(user)
            resp = sendSMS(user.user_name, user.otp, user.user_phone)
            user_id_new = request.session['user_id'] = user.user_id
            print(user_id_new)
            return redirect('otp')
    return render(request,'user/user-register.html')





def user_logout(request):
    logout(request)
    return redirect('user_login')


def student(request):
    status = ""
    predicted_status = ""

    if request.method == 'POST':
        gre = float(request.POST.get('gre'))
        toefl = float(request.POST.get('toefl'))
        university_rating = float(request.POST.get('university_rating'))
        sop = float(request.POST.get('sop'))
        lor = float(request.POST.get('lor'))
        cgpa = float(request.POST.get('cgpa'))
        research = 1 if request.POST.get('research') == 'yes' else 0
        research = float(research)
        
       

        with open('linear.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)

        feature_vector = [gre, toefl, university_rating, sop, lor, cgpa, research]

        predicted_status = loaded_model.predict([feature_vector])

        predicted_status = min(100, max(0, int(predicted_status * 100)))

    return render(request, 'user/student.html', {'status': predicted_status})



def forgot_password(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        if phone == "":
            messages.warning(request, 'Enter Number')
        else:
            try:
                user = User.objects.get(user_phone=phone)
                if user.status == "Accepted":
                    subject = "Password Reminder"
                    message = f"Your password is: {user.user_password}"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.user_email]  

                    send_mail(subject, message, from_email, recipient_list)

                    messages.info(request, "Your password has been sent to your email.")
                    request.session['user_id'] = user.user_id
                    return redirect('user_login')
                else:
                    messages.warning(request, 'You are not registered yet!')
                    return redirect('forgot')
            except User.DoesNotExist:
                messages.warning(request, 'You are not registered yet!')
                return redirect('forgot')
    return render(request, 'user/forgot-password.html')



def otp(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    
    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        print(otp_entered)
        user_id = request.session['user_id']
        print(user_id)

        if not otp_entered:
            messages.error(request, 'Please enter the OTP')
            print("OTP not entered")
            return redirect('otp')
        
        try:
            user = User.objects.get(user_id=user_id)
            if user.status == "Accepted":
                pass
            elif str(user.otp) == otp_entered:
                messages.success(request, 'OTP verification and Registration are successful!')
                user.status = "Verified"
                user.save()
                return redirect('user_login')
            
            else:
                messages.error(request, 'Invalid OTP entered')
                print("Invalid OTP entered")
                return redirect('otp')

        except User.DoesNotExist:
            messages.error(request, 'Invalid user')
            print("Invalid user")
            return redirect('user_register')

    return render(request, 'user/otp.html')


