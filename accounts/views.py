from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import date
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Clientscog.settings import EMAIL_PORT,EMAIL_HOST,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
from .models import OTP


# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('company dashboard')
        else:
            messages.info(request, "Invalid Credentials")
    return render(request, 'login.html/')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('Registeration-page')
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already taken")
                return redirect('Registeration-page')
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, \
                last_name=last_name, is_active=False)
            user.save()
            otp_sent = send_otp(user.email, user.id, user.username)
            if otp_sent:
                request.session['user_id'] = user.id
            return redirect('verification page') # 'accounts/login'#######################
        messages.info(request, "password not matched")
        return redirect('Registeration-page')
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def verify(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        otp_sent = request.POST['otp_sent']
        user_name = request.session.get('user_name_fpwd', False)
        print(user_id)
        if user_id:
            try:
                X = OTP.objects.get(user_id=user_id, otp=otp_sent)
                X.delete()
                user_obj = User.objects.get(id=user_id)
                user_obj.is_active = True
                user_obj.save()
                return redirect('login-Page')
            except:
                messages.error(request, "Invalid Verification OTP")
                print("exception")
                return redirect('verification page')
        elif user_name:
            try:
                U = User.objects.get(username=user_name)
                X = OTP.objects.get(user_id=U.pk, otp=otp_sent)
                X.delete()
                return redirect('forgot password')
            except:
                messages.error(request, "Invalid Verification OTP")
                print("exception2")
                return redirect('verification page')
    return render(request, 'email_verify.html')

def re_pass_username(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        try:
            U = User.objects.get(username=usern)
            otp_sent = send_otp(U.email, U.pk, U.username)
            request.session['user_name_fpwd'] = usern
            return redirect('verification page')
        except:
            messages.error(request, "Invalid User Name")
            print("exception")
            return render(request, 'forgot_password_username.html')
    else:
        return render(request, 'forgot_password_username.html')

def re_pass(request):
    if request.method == "POST":
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        if pwd1 == pwd2:
            user_name = request.session.get('user_name_fpwd')
            userObj = User.objects.get(username=user_name)
            userObj.set_password(pwd1)
            userObj.save()
            return redirect('login-Page')
    return render(request, 'forgot_password.html')

def verify_otp(request):
    return render(request, 'forgot_passwword_verify.html')

def send_otp(email, user_id, name):
    sender_address = EMAIL_HOST_USER
    sender_pass = EMAIL_HOST_PASSWORD
    receiver_address = email
    passd = random.randrange(111111, 10000000, 39)
    mail_content = "Hello your account verification code for the Username "+" "+str(name)+" "+"is :"+str(passd)
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Acount activation code'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print(passd)
    # user_id = user.id
    # print("user_id", user_id)
    otp1 = OTP(user_id_id=user_id, otp=passd)
    otp1.save()
    print('Mail Sent')
    return True