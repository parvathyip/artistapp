from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Login(AbstractUser):
    user_type=models.CharField(max_length=30)
    view_password=models.CharField(max_length=30)

class FreelancerReg(models.Model):
    f_log=models.ForeignKey(Login,on_delete=models.CASCADE)
    f_name=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    email=models.EmailField()
    experience=models.CharField(max_length=30)
    address=models.TextField()
    pin=models.CharField(max_length=6)
    f_status=models.CharField(max_length=30,default='Pending')

class Category(models.Model):
    category=models.CharField(max_length=30)
    image=models.ImageField()

class FreelancerCategory(models.Model):
    freelancer_id=models.ForeignKey(FreelancerReg,on_delete=models.CASCADE)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)

class Product(models.Model):
    freelancer_id=models.ForeignKey(FreelancerReg,on_delete=models.CASCADE)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    pimage=models.ImageField()
    pname=models.CharField(max_length=30)
    price=models.CharField(max_length=30)
    p_size=models.CharField(max_length=30)
    prodstatus=models.CharField(max_length=30,null=True,default='Pending')

class UserReg(models.Model):
    u_log=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    email=models.EmailField()
    housename=models.CharField(max_length=30,null=True)
    place=models.CharField(max_length=30,null=True)
    city=models.CharField(max_length=30,null=True)
    district=models.CharField(max_length=30,null=True)
    pin=models.CharField(max_length=30,null=True)

class Feedback(models.Model):
    user_id=models.ForeignKey(UserReg,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    review_text=models.CharField(max_length=30)
    feedback_date=models.DateField(auto_now_add=True,null=True)

class Cart(models.Model):
    user_id=models.ForeignKey(UserReg,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart_status=models.CharField(max_length=30,default='Pending')
    qty=models.CharField(max_length=30,default='1')
    total=models.CharField(max_length=30,default='0')
    pay_type=models.CharField(max_length=30,default='')
    payment_status=models.CharField(max_length=30,default='Pending')
    payment_date=models.DateField(null=True)
    order_date=models.DateField(auto_now_add=True,null=True)
    feedback_id=models.ForeignKey(Feedback,on_delete=models.CASCADE,null=True)

class RequestProduct(models.Model):
    user_id=models.ForeignKey(UserReg,on_delete=models.CASCADE,null=True)
    freelancer_id=models.ForeignKey(FreelancerReg,on_delete=models.CASCADE)
    requeststatus=models.CharField(max_length=30,default='Pending')
    reqrequirestatus=models.CharField(max_length=30,default='Pending')
    requestimage=models.ImageField()
    # requestname=models.CharField(max_length=30)
    requestdesc=models.TextField()
    requestsize=models.CharField(max_length=30)
    requestprice=models.CharField(max_length=30,null=True,default='')
    reqexpecteddate=models.DateField(null=True)
    reqcompletedate=models.DateField(null=True)
    payment_type=models.CharField(max_length=30,null=True,blank=True)
    payment_date=models.DateField(null=True,blank=True)

class Chat(models.Model):
    user_id=models.ForeignKey(UserReg,on_delete=models.CASCADE,null=True)
    freelancer_id=models.ForeignKey(FreelancerReg,on_delete=models.CASCADE)
    request_id=models.ForeignKey(RequestProduct,on_delete=models.CASCADE,null=True)
    message=models.CharField(max_length=30,null=True)
    reply=models.CharField(max_length=30,null=True)
    # reply_status=models.CharField(max_length=30,default='empty')

