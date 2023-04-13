from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import random 
from django.conf import settings
from .models import *
# Create your views here.

def beauty_fun(request):
    filtered_blogs = Blog.objects.filter(categories = 'beauty')
    try:
        user_obj = User.objects.get(email =  request.session['user_email'])
        return render(request, 'beauty.html', {'beauty': 'jivit', 'userdata':user_obj, 'blogs': filtered_blogs})
    except:
        return render(request, 'beauty.html', {'beauty': 'jivit', 'blogs': filtered_blogs })
    

def index_fun(request):
    try:
        global user_obj
        user_obj = User.objects.get(email =  request.session['user_email'])
        return render(request, 'index.html', {'home': 'jivit', 'userdata':user_obj})
    except:
        return render(request, 'index.html', {'home': 'jivit'})

def contact_fun(request):
    return render(request, 'contact.html' )

def fashion_fun(request):
    filtered_blogs = Blog.objects.filter(categories = 'fashion')
    try:
        user_obj = User.objects.get(email =  request.session['user_email'])
        return render(request, 'fashion.html', {'fashion': 'jivit', 'userdata':user_obj, 'blogs': filtered_blogs})
    except:
        return render(request, 'fashion.html', {'fashion': 'jivit', 'blogs': filtered_blogs})
    

def reg_function(request):
    return render(request, 'register.html')


def register_submit(request):
    
    if request.POST['passwd'] == request.POST['repasswd']:
        global g_otp, user_data
        user_data = [request.POST['fname'], 
                     request.POST['lname'],
                     request.POST['username'],
                     request.POST['email'],
                     request.POST['passwd']]
        g_otp = random.randint(100000, 999999)
        send_mail('Welcome Welcome',
                  f"Your OTP is {g_otp}",
                  settings.EMAIL_HOST_USER,
                  [request.POST['email']])
        return render(request, 'otp.html')        
    else:
        return render(request, 'register.html', {'msg': 'Both passwords do not MATCH'})


def otp_fun(request):
    try:
        if int(request.POST['u_otp']) == g_otp:
            User.objects.create(
                first_name = user_data[0],
                    last_name = user_data[1],
                    username = user_data[2],
                    email = user_data[3],
                    password = user_data[4])
            return render(request, 'register.html', {'msg':'Successfully Registered!!'})
        else:
            return render(request, 'otp.html', {'msg': 'Invalid OTP, Enter again!!!'})
    except:
        return render(request, 'register.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        #get() ye tumhe table mein se EK HI row zuupp karke 
        # de sakta hai 
        # 0 match mile ya to 1 se zyada match mile
        # get method error dega
        try:
            #agar niche wali line pe error aaya matalb email not found
            # get() wo row object return karega , r1 mein store kar dega
            
            user_obj = User.objects.get(email = request.POST['email'])

            if request.POST['passwd'] == user_obj.password:
                request.session['user_email'] = request.POST['email']
                return redirect('index')
            else:
                return render(request, 'login.html', {'msg': 'Invalid password'})
        except:
            return render(request, 'login.html', {'msg':'email is not registered!!'})


def logout(request):
    try:
        del request.session['user_email']
        global user_obj
        del user_obj
        return render(request, 'index.html', {'home': 'jivit'})
    except:
        return redirect('login')


def add_blog(request):
    if request.method == 'GET':
        try:
            return render(request, 'add_blog.html', {'userdata':user_obj})
        except:
            return redirect('login')
    else:
        Blog.objects.create(
            title = request.POST['title'],
            des = request.POST['des'],
            categories = request.POST['cate'],
            pic = request.FILES['foto'],
            #user ek foreign key field hai, isiliye obj dena hai
            user = user_obj
            #ye object jiska session chalu hai uska hai
        )
        return redirect('index')


def my_blogs(request):
    my_filtered_blogs = Blog.objects.filter(user = user_obj)
    return render(request, 'my_blogs.html', {'blogs':my_filtered_blogs, 'userdata':user_obj})


def singleblog(request, pk):
    s_blog = Blog.objects.get(id = pk)
    return render(request, 'single_blog.html', {"blog":s_blog, 'userdata':user_obj})