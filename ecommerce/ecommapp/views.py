from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import Products,Cart,Order
from django.db.models import Q
import random
import razorpay 
from django.core.mail import send_mail

# Create your views here.

def about(request):
   # return HttpResponse("Hello my name is ankit")
    #x='This is about page'
    #return HttpResponse(x)
    return render(request,'about.html')  

def contact(request):
    return render(request,'contact.html')

def delete(request,rid):
    print(rid)
    return HttpResponse('Id to be deleted')  

class ContactForm(View):
    def get(self,request,rid):
        print('Parameter is: ',rid)
        return HttpResponse('This is Contact page....!') 
    
def ankit(request):
    context={}
    context['data']='Hello we are passing string to html file'
    context['x']=300
    context['y']=0
    context['lst']=[10,20,30,40,45,46,47]
    context['product']=[{'id':1,'pname':'tomato',
    'type':'Vegitable','price':'50/kg'},
    {'id':2,'pname':'Suger','type':'Grosary','price':'55/kg'},
     {'id':3,'pname':'Haldi','type':'Grosary','price':'200/kg'},
      {'id':4,'pname':'Potato','type':'Vegitable','price':'20/kg'},
       {'id':5,'pname':'Iphone','type':'Mobile','price':90000},
        {'id':6,'pname':'Jeans','type':'Cloth','price':2000}]

    return render(request,'ankit.html',context)  

def base(request):
    return render(request,'base.html')  

def products(request):
    #uid=request.user.id
    #print(uid)
    p=Products.objects.filter(is_active=True)
    #print(p)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def register(request):
    context={}
    if request.method=="GET":
        return render(request,'register.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']
        cp=request.POST['ucpass']

        '''
        print(n)
        print(p)
        print(cp)
        return HttpResponse("Data fetched..!!")
        '''
        if n=='' or p=='' or cp=='':
            context['errmsg']="Field can not be blank"
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="Password & confirm password didn't match"
            return render(request,'register.html',context)
        elif len(p)<8:
            context['errmsg']="Password must be at least 8 character"
            return render(request,'register.html',context)
        else:
            try:
               u=User.objects.create(username=n,email=n)
               u.set_password(p)
               u.save()
               context['sucess']="User Created sucessfully"
               #return render(request,'register.html',context)
            except Exception:
                context['errmsg']='Username already Exist,Please Login'
                #return render(request,'register.html',context)

            return render(request,'register.html',context) 
        

def user_login(request): 
    if request.method=="GET":
        return render(request,'login.html')

    else:
        n=request.POST['uname']
        p=request.POST['upass']

        #print(n)
        #print(p)
        #return HttpResponse("Data Fetched..!!")
        u=authenticate(username=n,password=p) 
        #print(u) 

        if u is not None:
            login(request,u)
            return redirect('/products')
        else:
            context={}
            context['errmsg']='Invalid id Username or Password'
            return render(request,'login.html',context) 
        
def user_logout(request):
    logout(request)
    return redirect('/products')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)

    p=Products.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='1':
        #p=Products.objects.order_by('-price').filter(is_active=True)
        t=('-price')
    else:
        #p=Products.objects.order_by('price').filter(is_active=True)
        t=('price')

    p=Products.objects.order_by(t).filter(is_active=True)    
    context={}
    context['data']=p
    return render(request,'index.html',context) 

def pricefilter(request):   
    min=request.GET['min']
    max=request.GET['max']
    #print(min)
    #print(max) 

    q1=Q(price__gte=min)
    q2=Q(price__lte=max)  

    p=Products.objects.filter(q1 & q2) 

    context={}
    context['data']=p
    return render(request,'index.html',context)


def product_detail(request,pid):
    p=Products.objects.filter(id=pid) 
    context={}
    context['data']=p
    return render (request,'product_details.html',context) 

def cart(request,pid):
    if request.user.is_authenticated:
        #uid=request.user.id
        u=User.objects.filter(id=request.user.id)
        #print(u)
        #print(u[0])
        
        p=Products.objects.filter(id=pid)
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['data']=p
        if n==1:
            context['msg']='Product already exist in cart'

        else:    
            c=Cart.objects.create(pid=p[0],userid=u[0])
            c.save()
            #return HttpResponse("Data Stored")
           
            context['msg']='Product added successfully in cart'
        return render(request,'product_details.html',context)
    
    else:
        return redirect('/login')
    
def viewcart(request):
    c=Cart.objects.filter(userid=request.user.id)
    #print(c[0].userid.is_staff)
    #print(c[0].pid.name)
    #return HttpResponse("Data fetched")
    sum=0
    for x in c:
        sum=sum+x.pid.price*x.qty
    context={}
    context['data']=c
    context['total']=sum
    context['n']=len(c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    #print(q)
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1

    c.update(qty=q)
    return redirect('/viewcart')   


def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    print(c)
    orderid=random.randrange(1000,9999)

    for x in c:
        amount=x.qty*x.pid.price
        o=Order.objects.create(orderid=orderid,pid=x.pid,userid=x.userid,qty=x.qty,amt=amount)
        o.save()
        x.delete()

    return redirect('/fetchorder')
def fetchorder(request):
    o=Order.objects.filter(userid=request.user.id)
    context={}
    context['data']=o
    sum=0
    for x in o:
        sum=sum+x.amt
    context['total']=sum
    context['n']=len(o)    
    return render(request,'placeorder.html',context) 

def makepayment(request):

    client = razorpay.Client(auth=("rzp_test_gbSnn9SYBjH87Y", "pjgnFozwt3nqDzMlkYHCo18k"))

    o=Order.objects.filter(userid=request.user.id)
    sum=0
    for x in o:
        sum=sum+x.amt
        oid=x.orderid

    data = { "amount": sum*100, "currency": "INR", "receipt": oid}
    payment = client.order.create(data=data)
    #print(payment)
    context={}
    context['payment']=payment
    return render(request,'pay.html',context) 

def paymentsuccess(request):
    sub="Ekart_order Status"
    msg='Thanks for shopping...!!!'
    frm ='ankitgsingh30@gmail.com'

    u=User.objects.filter(id=request.user.id)
    to=u[0].email

    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False

    )
    return render(request,'paymentsuccess.html') 


def search(request):
    query=request.GET['query']
    pname=Products.objects.filter(name__icontains=query)
    pcat=Products.objects.filter(cat__icontains=query)
    pdetail=Products.objects.filter(pdetail__icontains=query)

    allproducts=pname.union(pcat,pdetail)
    context={}

    if allproducts.count()==0:
        context['msg']='Product Not Found'
    context['data']=allproducts
    return render(request,'index.html',context)    




