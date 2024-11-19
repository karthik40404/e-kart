from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os

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
        data=Product.objects.all()
        return render(req,'shop/home.html',{'products':data})
    else:
        return redirect(log)

def log_out(req):
    logout(req)
    req.session.flush()
    return redirect(log)

def addproduct(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            disc=req.POST['disc']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            stock=req.POST['stock']
            file=req.FILES['img']
            data=Product.objects.create(pid=pid,name=name,disc=disc,price=price,offer_price=offer_price,stock=stock,img=file)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/addp.html')
    else:
        return redirect(log)


def edit_product(req,pid):
    if req.method=='POST':
        p_id=req.POST['pid']
        name=req.POST['name']
        disc=req.POST['disc']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        file=req.FILES.get('img')
        if file:
            Product.objects.filter(pk=pid).update(pid=p_id,name=name,disc=disc,price=price,offer_price=offer_price,stock=stock)
            data=Product.objects.get(pk=pid)
            data.img=file
            data.save()
        else: 
            Product.objects.filter(pk=pid).update(pid=p_id,name=name,disc=disc,price=price,offer_price=offer_price,stock=stock)
        return redirect (shop_home)
    
    else:
        data=Product.objects.get(pk=pid)
        return render(req,'shop/edit.html',{'data':data})

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

def reg(req):
    return render(req,'user/reg.html')

def uhome(req):
    return render(req,'user/uhome.html')
