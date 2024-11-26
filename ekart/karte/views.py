from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

# Create your views here.
def log(req):
    if 'shop' in req.session:
        return redirect (shop_home)
    if 'user' in req.session:
        return redirect (uhome)
    if req.method=='POST':
        uname=req.POST['uname']
        psw=req.POST['psw']
        data=authenticate(username=uname,password=psw)
        print(data)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=uname
                return redirect(shop_home)
            else:
                req.session['user']=uname
                return redirect(uhome)
        else:
            messages.warning(req, "Incorrect uname or password.")
            return redirect(log)
    return render(req,'login.html')

def log_out(req):
    logout(req)
    req.session.flush()
    return redirect(log)

#----------------------------admin
def shop_home(req):
    if 'shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'products':data})
    else:
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

#-----------------------user
def reg(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        psw=req.POST['psw']
        try:
            data=User.objects.create_user(first_name=name,email=email,username=email,password=psw)
            data.save()
        except:
             messages.warning(req, "email already in use")
             return redirect(reg)
        return redirect(log)
    else:
        return render(req,'user/reg.html')

def uhome(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/uhome.html',{'products':data})
    else:
        return redirect(log)
    
def viewp(req,pid):
    data=Product.objects.get(pk=pid)
    return render(req,'user/vproduct.html',{'product':data})

#-----------------------cart

def addtocart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(viewc)

def viewc(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)[::-1]
    return render(req,'user/cart.html',{'cart':data})

def qin(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()
    return redirect(viewc)

def qout(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(viewc)

def cart_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def buybuy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def bookings(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]

    return render(req,'user/book.html',{'bookings':buy})

def view_book(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'user/vbook.html',{'bookings':buy})
