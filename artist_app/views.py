from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
from datetime import datetime
# Create your views here.
def index(request):
    return render(request,'index.html')
def users_login(request):
    if request.POST:
        name=request.POST['uname']
        passwd=request.POST['pwd']
        user=authenticate(username=name,password=passwd)
        if user is not None:
            if user.user_type=='admin':
                msg='Welcome to admin dashboard'
                messages.success(request,msg)
                return redirect('/admin-dashboard')
            elif user.user_type=='freelancer':
                request.session['fid']=user.id
                msg='Welcome to freelancer dashboard'
                messages.success(request,msg)
                return redirect('/freelancer-dashboard')
            elif user.user_type=='user':
                request.session['uid']=user.id
                msg='Welcome to user dashboard'
                messages.success(request,msg)
                return redirect('/user-dashboard')
        else:
            msg='Invalid username or password'
            messages.success(request,msg)
            return redirect('/users-login')    
    return render(request,'users_login.html')
#admin
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')
def admin_freelancerapprove(request):
    pending_freelancers=FreelancerReg.objects.filter(f_status='Pending')
    if request.POST:
        fids=request.POST.getlist('approves')
        for fid in fids:
            freelancer=FreelancerReg.objects.filter(id=fid).update(f_status='Approved')
            freelancer=FreelancerReg.objects.get(id=fid).f_log
            flogin=Login.objects.filter(username=freelancer).update(is_active=1)
    return render(request,'admin/admin_freelancerapprove.html',{'freelancers':pending_freelancers})
def admin_viewfreelancers(request):
    approved_freelancers=FreelancerReg.objects.filter(f_status='Approved')
    return render(request,'admin/admin_viewfreelancers.html',{'freelancers':approved_freelancers})
def admin_delete(request):
    fid=request.GET.get('freelancer')
    print(fid,'fiddddddddddddd')
    freelancerlog=FreelancerReg.objects.get(id=fid).f_log
    freelancer=FreelancerReg.objects.filter(id=fid).delete()
    flogin=Login.objects.filter(username=freelancerlog).delete()
    msg='Freelancer Deleted Sucessfully'
    messages.success(request,msg)
    return redirect('/admin-viewfreelancers')  
def admin_addcategories(request):
    categories=Category.objects.all()
    if request.POST:
        category=request.POST['cname']
        image=request.FILES['cimage']
        category=Category.objects.create(category=category,image=image)
        category.save()
    return render(request,'admin/admin_addcategories.html',{'categories':categories})  
def admin_update_category(request):
    categoryid=request.GET.get('catid')
    category=Category.objects.filter(id=categoryid)
    if request.POST:
        categoryupdate=Category.objects.get(id=categoryid)
        categoryupdate.name=request.POST['cname']
        if 'cimage' in request.FILES:
            categoryupdate.image=request.FILES['cimage']
        else:
            categoryupdate.image=category[0].image
        categoryupdate.save()
        msg='Category Updated Sucessfully'
        messages.success(request,msg)
        return redirect('/admin-addcategories')
    return render(request,'admin/admin_updatecategory.html',{'category':category})
def admin_delete_category(request):
    categoryid=request.GET.get('catid')
    category=Category.objects.filter(id=categoryid).delete()
    msg='Category Deleted Sucessfully'
    messages.success(request,msg)
    return redirect('/admin-addcategories')
def admin_viewfeedbacks(request):
    feedbacks=Feedback.objects.all()
    product_ids = feedbacks.values_list('product_id', flat=True).distinct()
    products = Product.objects.filter(id__in=product_ids)    
    print(feedbacks,'feedbacks,,,,,,,')
    return render(request,'admin/admin_viewfeedbacks.html',{"feedbacks":feedbacks,'products':products})
def admin_viewpayments(request):
    carts=Cart.objects.filter(cart_status='Completed')
    requests=RequestProduct.objects.filter(requeststatus='Paid')
    return render(request,'admin/admin_viewpayments.html',{'carts':carts,'requests':requests})
#freelancer
def freelancer_register(request):
    if request.POST:
        fname=request.POST['fullname']
        phone=request.POST['phone']
        email=request.POST['email']
        exp=request.POST['exp']
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        address=request.POST['address']
        pin=request.POST['pin']
        if Login.objects.filter(username=uname,password=pwd).exists():
            # msg='Already Taken'
            # messages.success(request,msg)
            # return redirect('/freelancer-register')
            pass
        else:
            try:
                flog=Login.objects.create_user(username=uname,password=pwd,view_password=pwd,user_type='freelancer',is_active=0)
                flog.save()
                freg=FreelancerReg.objects.create(f_log=flog,f_name=fname,phone=phone,email=email,experience=exp,address=address,pin=pin)
                freg.save()
                msg='Freelancer Register sucessfully Wait for Approval!'
                messages.success(request,msg)
                return redirect('/freelancer-register')
            except:
                msg='Already Taken'
                messages.success(request,msg)
                return redirect('/freelancer-register')
    return render(request,'freelancer_register.html')
def freelancer_dashboard(request):
    return render(request,'freelancer/freelancer_dashboard.html')
def freelancer_updateprofile(request):
    freelancer=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=freelancer)
    print(fdata,'freelancer,,,,,,,,,,,')
    if request.POST:
        fname=request.POST['fullname']
        phone=request.POST['phone']
        email=request.POST['email']
        exp=request.POST['exp']
        address=request.POST['address']
        pin=request.POST['pin']
        fdata=FreelancerReg.objects.filter(f_log_id=freelancer).update(f_name=fname,phone=phone,email=email,experience=exp,address=address,pin=pin)
        msg='Freelancer Updated sucessfully!'
        messages.success(request,msg)
        return redirect('/freelancer-updateprofile')
    return render(request,'freelancer/freelancer_updateprofile.html',{'fdata':fdata})
def freelancer_addcategory(request):
    categorystr=''
    categories=Category.objects.all()
    freelancer=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=freelancer)
    fcat=FreelancerCategory.objects.filter(freelancer_id=fdata)
    if request.POST:
        categorylist=request.POST.getlist('cats')
        print(categorylist,'categorylist,,,,,,,,,,,')
        for category in categorylist:
            print(category,'category,,,,,,,,,,,,,,,')
            if FreelancerCategory.objects.filter(freelancer_id=fdata,category_id_id=category).exists():
                msg='Category already added'
                messages.success(request,msg)
            else:
                cat=FreelancerCategory.objects.create(freelancer_id=fdata,category_id_id=category)
                cat.save()
                msg='Category addedd sucessfully!'
                messages.success(request,msg)
            return redirect('/freelancer-addcategory')
    current=FreelancerReg.objects.filter(f_log_id=freelancer)
    return render(request,'freelancer/freelancer_addcategory.html',{'categories':categories,'current':current,'fcategories':fcat})
def freelancer_addproducts(request):
    flog=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=flog)
    freelancer_categories=FreelancerCategory.objects.filter(freelancer_id=fdata)
    if request.POST:
        category=request.POST['cat']
        image=request.FILES['pimage']
        pname=request.POST['prodname']
        pprice=request.POST['prodprice']
        psize=request.POST['prodsize']
        print(category,image,pname,pprice,psize,',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
        prod=Product.objects.create(freelancer_id=fdata,category_id_id=category,pimage=image,pname=pname,price=pprice,p_size=psize)
        prod.save()
        msg='Your Product addedd sucessfully!'
        messages.success(request,msg)
        return redirect('/freelancer-addproducts')
    return render(request,'freelancer/freelancer_addproducts.html',{'categories':freelancer_categories})
def freelancer_viewproducts(request):
    flog=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=flog)
    freelancer_categories=FreelancerCategory.objects.filter(freelancer_id=fdata)
    category=request.GET.get('category')
    print(category,'category,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*')
    if category:
        products=Product.objects.filter(category_id_id=category,freelancer_id=fdata)
    else:
        products=Product.objects.filter(freelancer_id=fdata)
    print(products,'//////')
    return render(request,'freelancer/freelancer_viewproducts.html',{'categories':freelancer_categories,'products':products})
def freelancer_view_catproducts(request):
    flog=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=flog)
    category=request.GET.get('catid')
    print(category,'category,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*')
    return redirect('/freelancer-viewproducts?category='+category)
def freelancer_viewrequests(request):
    flog=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=flog)
    requests=RequestProduct.objects.filter(freelancer_id=fdata)
    return render(request,'freelancer/freelancer_viewrequests.html',{'requests':requests})
def freelancer_acceptrequest(request):
    req=request.GET.get('rid')
    requests=RequestProduct.objects.filter(id=req).update(requeststatus='Accepted')
    return redirect('/freelancer-addrequestprice?rid='+req)
def freelancer_addrequestprice(request):
    req=request.GET.get('rid')
    if request.POST:
        price=request.POST['prodprice']
        comdate=request.POST['prodcompletedate']
        requests=RequestProduct.objects.filter(id=req).update(requestprice=price,reqcompletedate=comdate)
        msg='Request accepted and price,date added!'
        messages.success(request,msg)
        return redirect('/freelancer-viewrequests')
    return render(request,'freelancer/freelancer_addrequestprice.html')
def freelancer_rejectrequest(request):
    req=request.GET.get('rid')
    requests=RequestProduct.objects.filter(id=req).update(requeststatus='Rejected')
    print(requests,'reqqqqqqqqq')
    msg='Request rejected!'
    messages.success(request,msg)
    return redirect('/freelancer-viewrequests')
def freelancer_completerequest(request):
    req=request.GET.get('rid')
    requests=RequestProduct.objects.filter(id=req).update(requeststatus='Completed')
    print(requests,'reqqqqqqqqq')
    msg='Your work has been completed!'
    messages.success(request,msg)
    return redirect('/freelancer-viewrequests')
def freelancer_viewproductdetail(request):
    prod=request.GET.get('prod')
    productdata=Product.objects.get(id=prod)
    feedbacks = Feedback.objects.filter(product_id=productdata)
    print(feedbacks,'fffffffffffff,,,,,,,,,,')
    return render(request,'freelancer/freelancer_viewproductdetail.html',{"product":productdata,'feedbacks':feedbacks})
    # return render(request,'freelancer/freelancer_viewproductdetail.html')
def freelancer_viewproducthistory(request):
    products=Cart.objects.filter(cart_status="Completed")

    return render(request,'freelancer/freelancer_viewproducthistory.html',{'products':products})
def freelancer_viewchats(request):
    flog=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=flog)
    fchats=Chat.objects.filter(freelancer_id=fdata)
    print(fchats,'chatss')
    return render(request,'freelancer/freelancer_viewchats.html',{'fchats':fchats})

def freelancer_viewchatdetailed(request):
    cuserid=request.GET.get('chatuser')
    print(cuserid,'cuserid,,,,,,,,,,')
    flog=request.session['fid']
    fdata=FreelancerReg.objects.get(f_log_id=flog)
    userchats=Chat.objects.filter(user_id_id=cuserid)
    request_id=userchats[0].request_id
    if request.POST:
        freply=request.POST['reply']
        rid=(request.POST['rid'])
        print(freply,rid)
        newchat=Chat.objects.create(user_id_id=cuserid,freelancer_id=fdata,request_id_id=rid,reply=freply)
        newchat.save()
    return render(request,'freelancer/freelancer_viewchatdetailed.html',{'userchats':userchats,'request':request_id})
#user
def user_register(request):
    if request.POST:
        name=request.POST['fullname']
        phone=request.POST['phone']
        email=request.POST['email']
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        hname=request.POST['housename']
        place=request.POST['place']
        city=request.POST['city']
        district=request.POST['district']
        pin=request.POST['pin']
        if Login.objects.filter(username=uname,password=pwd).exists():
            print('yes,,,,,,,,,,,,,,,,,,,,,,,,')
        try:
            ulog=Login.objects.create_user(username=uname,password=pwd,view_password=pwd,user_type='user')
            ulog.save()
            ureg=UserReg.objects.create(u_log=ulog,name=name,phone=phone,email=email,housename=hname,place=place,city=city,district=district,pin=pin)
            ureg.save()
            msg='User Register sucessfully Please Login to access!'
            messages.success(request,msg)
            return redirect('/users-login')
        except:
            msg='Already Taken'
            messages.success(request,msg)
            return redirect('/user-register')
    return render(request,'user_register.html')
def user_dashboard(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    categories=Category.objects.all()
    category=request.GET.get('category')
    if category:
        products=Product.objects.filter(category_id_id=category)
    else:
        products=Product.objects.all().order_by('category_id')
    c_count=0
    if c_count != 0:
        c_count=request.GET.get('c_count')
    if c_count:
        pass
    elif c_count == 0 or c_count == None:
        cartnumber=Cart.objects.filter(user_id=udata,cart_status='Carted')
        c_count=len(cartnumber)
        print(c_count,'c_count')
    return render(request,'user/user_dashboard.html',{'categories':categories,'products':products,'c_count':c_count})
def user_viewcatproducts(request):
    category=request.GET.get('catid')
    return redirect('/user-dashboard?category='+category)
def user_viewcategories(request):
    categories=Category.objects.all()
    return render(request,'user/user_viewcategories.html',{'categories':categories})
def user_addcart(request):
    prod = request.GET.get('prod')
    product=Product.objects.get(id=prod)
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    print(product,udata,',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*')
    cno=0
    if Cart.objects.filter(user_id=udata,product_id=product,cart_status='Carted').exists():
        msg='Product already added to cart'
        messages.success(request,msg)
    else:
        cartitem=Cart.objects.create(user_id=udata,product_id=product,cart_status='Carted',total=product.price)
        cartitem.save()
        # print(product.price,'priccccccccccccccccc')
        cartnumber=Cart.objects.filter(user_id=udata,cart_status='Carted')
        cno=len(cartnumber)
        print(cno,'cno')
    category_id = request.GET.get('category')
    msg='Product added to cart sucessfully'
    messages.success(request,msg)
    return redirect('/user-dashboard?category=' + category_id + '&c_count=' +str(cno))
def user_viewcart(request):
    subtotal=0
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    carts=Cart.objects.filter(user_id=udata,cart_status='Carted')
    if request.POST:
        quantity=request.POST['quantity']
        print(quantity,'quantity,,,,,,,,,,,,,,,,,,,')
        ulog=request.session['uid']
        udata=UserReg.objects.get(u_log_id=ulog)
        cartid=request.POST['cart_id']
        print(cartid,'cartid,,,,,,,,,,,,,,,,,,,,,,,,,')
        updated=Cart.objects.get(id=cartid,user_id=udata)#.update(qty=quantity,total=product.price)
        productprice=updated.product_id.price
        curr_total=int(productprice)*int(quantity)
        print(curr_total,'/.............................')
        updated.qty=quantity
        updated.total=curr_total
        updated.save()
        msg='Quantity Updated sucessfully'
        messages.success(request,msg)
        return redirect('/user-viewcart')
    for cart in carts:
        subtotal += int(cart.total)
    print(subtotal,'ssssssssssssssssssssssssss')
    return render(request,'user/user_viewcart.html',{'carts':carts,'subtotal':subtotal})
def user_removecartproduct(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    cartid=request.GET.get('cartid')
    removed=Cart.objects.filter(id=cartid,user_id=udata).delete()
    msg='Product removed from cart sucessfully'
    messages.success(request,msg)
    return redirect('/user-viewcart')
def user_payment(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    carts=Cart.objects.filter(user_id=udata,cart_status='Carted')
    product=carts[0].product_id
    if request.POST:
        type=request.POST['ptype']
        # cid=request.POST.get('')
        print(type,'type...........................')
        if type=='UPI':
            return redirect('/upi-form')
        elif type=='Credit/Debit Card':
            return redirect('/credit-form')
    return render(request,'user/user_payment.html',{'carts':carts})
def upi_form(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    carts=Cart.objects.filter(user_id=udata,cart_status='Carted')
    if carts:
        product=carts[0].product_id
        print(carts,product,'from upiiiiiiiiiiiiiiiiiii')
        if request.POST:
            dateofaction=datetime.today().date()
            print(dateofaction,'/////////////,,,,,')
            cart_update=carts.update(cart_status='Completed',pay_type="UPI",payment_date=dateofaction,payment_status='Completed')
            print(product,'ppppppppppppppppppppppppp')
            product_update=Product.objects.filter(id=product.id).update(prodstatus='Completed')
            msg='Payment sucessfull'
            messages.success(request,msg)
            return redirect('/user-viewcart')
    else:
        print('not from cart/////////////')
        req=request.GET.get('requestid')
        print(req)
        if request.POST:
            print('hiiiiii')
            dateofaction=datetime.today().date()
            print(dateofaction,'/////////////,,,,,')
            requests=RequestProduct.objects.filter(id=req).update(requeststatus='Paid',payment_type="UPI",payment_date=dateofaction)
            print(requests,'reqqqqqqqqq')
            msg='Paid Sucessfully!'
            messages.success(request,msg)
            return redirect('/user-viewrequests')
    return render(request,'user/upi_form.html')
def credit_form(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    carts=Cart.objects.filter(user_id=udata,cart_status='Carted')
    if carts:
        product=carts[0].product_id
        print(carts,product,'from upiiiiiiiiiiiiiiiiiii')
        if request.POST:
            dateofaction=datetime.today().date()
            print(dateofaction,'/////////////,,,,,')
            cart_update=carts.update(cart_status='Completed',pay_type="Credit/Debit Card",payment_date=dateofaction,payment_status='Completed')
            print(product,'ppppppppppppppppppppppppp')
            product_update=Product.objects.filter(id=product.id).update(prodstatus='Completed')
            msg='Payment sucessfull'
            messages.success(request,msg)
            return redirect('/user-viewcart')
    else:
        print('not from cart/////////////')
        req=request.GET.get('requestid')
        print(req)
        if request.POST:
            print('hiiiiii')
            dateofaction=datetime.today().date()
            print(dateofaction,'/////////////,,,,,')
            requests=RequestProduct.objects.filter(id=req).update(requeststatus='Paid',payment_type="Credit/Debit Card",payment_date=dateofaction)
            print(requests,'reqqqqqqqqq')
            msg='Paid Sucessfully!'
            messages.success(request,msg)
            return redirect('/user-viewrequests')
    return render(request,'user/credit_form.html')
def user_viewhistory(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    carts=Cart.objects.filter(user_id=udata,cart_status='Completed')
    requests=RequestProduct.objects.filter(user_id=udata,requeststatus='Paid')
    return render(request,'user/user_viewhistory.html',{'carts':carts,'requests':requests})
def user_addreview(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    cart=request.GET.get('cartid')
    if cart:
        cartdata=Cart.objects.filter(id=cart)
        productid=cartdata[0].product_id
    else:
        productidd=request.GET.get('prod')
        productid = Product.objects.get(id=productidd)
        print(productid,'elseeeeeeeeeee')
        if Feedback.objects.filter(product_id_id=productidd,user_id=udata).exists():
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            msg='Review already Added'
            messages.success(request,msg)
            return redirect('/user-viewproductdetail?prod='+productidd)
    if request.POST:
        review=request.POST['review']
        print(review,'review,,,,,,,,,,,,,,,,,,,,,')
        reviewadd=Feedback.objects.create(review_text=review,user_id=udata,product_id=productid)
        reviewadd.save()
        if cart:
            cartupdated=Cart.objects.filter(id=cart).update(feedback_id=reviewadd)
            msg='Review Added Sucessfully'
            messages.success(request,msg)
            return redirect('/user-viewhistory')
        else:
            msg='Review Added Sucessfully'
            messages.success(request,msg)
            return redirect('/user-viewproductdetail?prod='+productidd)
        
    return render(request,'user/user_addreview.html')
def user_updatereview(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    cart=request.GET.get('cartid')
    cartdata=Cart.objects.filter(id=cart)
    feedbackid=cartdata[0].feedback_id
    if request.POST:
        review=request.POST['upreview']
        print(review,'review,,,,,,,,,,,,,,,,,,,,,')
        feedbackid.review_text=review
        feedbackid.save()
        msg='Review updated Sucessfully'
        messages.success(request,msg)
        return redirect('/user-viewhistory')
    return render(request,'user/user_updatereview.html',{'cartdata':cartdata})
def user_viewproductdetail(request):
    prod=request.GET.get('prod')
    productdata=Product.objects.get(id=prod)
    feedbacks = Feedback.objects.filter(product_id=productdata)
    print(feedbacks,'fffffffffffff,,,,,,,,,,')
    return render(request,'user/user_viewproductdetail.html',{"product":productdata,'feedbacks':feedbacks})
def user_viewfreelancers(request):
    freelancers=FreelancerReg.objects.all()
    return render(request,'user/user_viewfreelancers.html',{'freelancers':freelancers})
def user_viewmoreworks(request):
    id=request.GET.get('fid')
    fdata=FreelancerReg.objects.get(id=id)
    products=Product.objects.filter(freelancer_id=fdata)
    return render(request,'user/user_viewmoreworks.html',{'products':products})
def user_makerequest(request):
    ulog=request.session['uid']
    udata=UserReg.objects.get(u_log_id=ulog)
    id=request.GET.get('fid')
    print(id,'makerequestttttttttttt')
    fdata=FreelancerReg.objects.get(id=id)
    print(udata,fdata,'00000000000000000000')
    if request.POST:
        image=request.FILES['pimage']
        # pname=request.POST['prodname']
        pprice=request.POST['proddesc']
        psize=request.POST['prodsize']
        pdate=request.POST['proddate']
        yourprod=RequestProduct.objects.create(user_id=udata,freelancer_id=fdata,reqexpecteddate=pdate,requestimage=image,requestdesc=pprice,requestsize=psize)
        yourprod.save()
        msg='Your Product request send sucessfully!'
        messages.success(request,msg)
        return redirect('/user-viewfreelancers')
    return render(request,'user/user_makerequest.html')
def user_viewrequests(request):
    ulog=request.session['uid']
    print(ulog,'ulog,,,,,,,,,,,,,,')
    udata=UserReg.objects.get(u_log_id=ulog)
    requests=RequestProduct.objects.filter(user_id=udata)
    return render(request,'user/user_viewrequest.html',{'requests':requests})
def user_payrequest(request):
    req=request.GET.get('rid')
    print(req)
    requestqry=RequestProduct.objects.get(id=req)
    # requests=RequestProduct.objects.filter(id=req).update(requeststatus='Paid')
    # print(requests,'reqqqqqqqqq')
    # msg='Paid Sucessfully!'
    # messages.success(request,msg)
    # return redirect('/user-viewrequests')
    if request.POST:
        type=request.POST['ptype']
        # cid=request.POST.get('')
        print(type,'type...........................')
        if type=='UPI':
            return redirect('/upi-form?requestid='+req)
        elif type=='Credit/Debit Card':
            return redirect('/credit-form?requestid='+req)
    return render(request,'user/user_requestpyment.html',{'requestdata':requestqry})
def user_acceptrequire(request):
    req=request.GET.get('rid')
    requests=RequestProduct.objects.filter(id=req).update(reqrequirestatus='Accepted')
    print(requests,'reqqqqqqqqq')
    msg='Requirements accepted Sucessfully!'
    messages.success(request,msg)
    return redirect('/user-viewrequests')
def user_rejectrequire(request):
    req=request.GET.get('rid')
    requests=RequestProduct.objects.filter(id=req).update(reqrequirestatus='Rejected',requeststatus='Rejected')
    print(requests,'reqqqqqqqqq')
    msg='Requirements Rejected!'
    messages.success(request,msg)
    return redirect('/user-viewrequests')

def user_freelancerchat(request):
    req=request.GET.get('rid')
    requests=RequestProduct.objects.get(id=req)
    fid=requests.freelancer_id
    ulog=request.session['uid']
    print(ulog,'ulog,,,,,,,,,,,,,,')
    udata=UserReg.objects.get(u_log_id=ulog)
    print(fid,udata,requests,'***************************')
    if request.POST:
        message=request.POST['msge']
        newchat=Chat.objects.create(user_id=udata,freelancer_id=fid,request_id=requests,message=message)
        newchat.save()
        print('sucesssss')
    prevchats=Chat.objects.filter(user_id=udata,freelancer_id=fid)
    print(prevchats,'previous,,,,,,,,,,,,,,,')
    return render(request,'user/user_freelancerchat.html',{'chats':prevchats})
