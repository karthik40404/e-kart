from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def log(req):
    if req.method=='POST':
        uname=req.POST['uname']
        psw=req.POST['psw']
        data=authenticate(username=uname,password=psw)
        print(data)
        if data:
            login(req,data)
            return redirect(shop_home)
        else:
            messages.warning(req, "Your account expires in three days.")
            return redirect(log)
    return render(req,'login.html')

def shop_home(req):
    return render(req,'shop/home.html')






def reg(req):
    return render(req,'reg.html')
