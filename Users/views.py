from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from .models import UserProfile

def register(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        address=request.POST.get('address')

        if User.objects.filter(username=username).exists():
            return render(request,'register.html',{"error":"user already exists"})
        user= User.objects.create_user(username=username,password=password,email=email)
        UserProfile.objects.create(user=user, address=address)
        return redirect("login")
    
    return render(request,"register.html")

def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('chat')
        else:
            return render(request,'login.html',{'error':'Invalid credentials'})
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')