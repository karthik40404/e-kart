from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def log(req):
    if 'shop' in req.session:
        return redirect (shop_home)
    if req.method=='POST':
        uname=req.POST['uname']
        psw=req.POST['psw']
        data=authenticate(username=uname,password=psw)
        print(data)
        if data:
            login(req,data)
            req.session['shop']=uname
            return redirect(shop_home)
        else:
            messages.warning(req, "Incorrect uname or password.")
            return redirect(log)
    return render(req,'login.html')

def shop_home(req):
    if 'shop' in req.session:
        return render(req,'shop/home.html')
    else:
        return redirect(log)

def log_out(req):
    logout(req)
    req.session.flush()
    return redirect(log)






def reg(req):
    return render(req,'reg.html')
