from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from datetime import datetime
# Create your views here.

def index(request):
    return render(request,"index.html")


def login(request):
    if request.POST:
        uname=request.POST["uname"]
        psw=request.POST["psw"]
        user=authenticate(username=uname,password=psw)
        
        print(user)
        if user:
            userdata=User.objects.get(username=uname)
            if user.is_active:
                if userdata.is_superuser == 1:
                        return redirect("/adminhome")
                else:
                        request.session["email"]=uname
                        r = Registration.objects.get(email=uname)
                        request.session["id"]=r.id
                        request.session["name"]=r.name
                        return redirect("/userhome")
            else:
                messages.info(request,"Not Approved")

            
        else:
            messages.info(request,"User dosent exist or invalid credentials")
    return render(request,"login.html")


def register(request):
    if request.POST:
        name=request.POST["name"]
        con=request.POST["con"]
        email=request.POST["email"]
        add=request.POST["add"]
        age=request.POST["age"]
        file=request.FILES["file"]
        psw=request.POST["psw"]
        user=User.objects.filter(username=email).exists()
        if user:
            messages.info(request,"User already exists")
        else:
            try:
                u=User.objects.create_user(username=email,email=email,password=psw)
                u.save()
            except Exception as e:
                messages.info(request,e)
            else:
                try:
                    s=Registration.objects.create(name=name,phone=con,email=email,address=add,user=u,age=age,idproof=file)
                    s.save()
                except Exception as e:
                    messages.info(request,e)
                else:
                    messages.info(request,"Registered successfully")
    return render(request,"register.html")


def adminhome(request):
    return render(request,"adminhome.html")

def adminusers(request):
    data = Registration.objects.all()
    return render(request,"adminusers.html", {"data":data})

def admindetections(request):
    data = Detections.objects.all()
    return render(request,"admindetections.html", {"data":data})









def userhome(request):
    id = request.session["id"]
    u = Registration.objects.get(id=id)
    uname = u.name
    return render(request,"userhome.html",{"uname":uname})

def userdetect(request):
    id = request.session["id"]
    u = Registration.objects.get(id=id)
    if request.POST:
        image = request.FILES['image']
        from underwaterApp.det import main
        det = Detections.objects.create(Registration=u,image=image)
        det.save()
        cImg = det.image
        result = main(cImg)
        print(result)
        det.results = result
        det.save()
        return redirect("/userhistory")
    return render(request,"userdetect.html")

def userhistory(request):
    id = request.session["id"]
    u = Registration.objects.get(id=id)
    data = Detections.objects.filter(Registration=u).order_by("-id")
    return render(request, "userhistory.html", {"data":data})















