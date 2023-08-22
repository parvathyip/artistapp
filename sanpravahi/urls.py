"""
URL configuration for sanpravahi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from artist_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('users-login/',views.users_login),
    #admin
    path('admin-dashboard/',views.admin_dashboard),
    path('admin-freelancerapprove/',views.admin_freelancerapprove),
    path('admin-viewfreelancers/',views.admin_viewfreelancers),
    path('admin-delete/',views.admin_delete),
    path('admin-addcategories/',views.admin_addcategories),
    path('admin-update-category/',views.admin_update_category),
    path('admin-delete-category/',views.admin_delete_category),
    path('admin-viewfeedbacks/',views.admin_viewfeedbacks),
    path('admin-viewpayments/',views.admin_viewpayments),
    #freelancer
    path('freelancer-register/',views.freelancer_register),
    path('freelancer-dashboard/',views.freelancer_dashboard),
    path('freelancer-updateprofile/',views.freelancer_updateprofile),
    path('freelancer-addcategory/',views.freelancer_addcategory),
    path('freelancer-addproducts/',views.freelancer_addproducts),
    path('freelancer-viewproducts/',views.freelancer_viewproducts),
    path('freelancer-view-catproducts/',views.freelancer_view_catproducts),
    path('freelancer-viewrequests/',views.freelancer_viewrequests),
    path('freelancer-acceptrequest/',views.freelancer_acceptrequest),
    path('freelancer-addrequestprice/',views.freelancer_addrequestprice),
    path('freelancer-rejectrequest/',views.freelancer_rejectrequest),
    path('freelancer-completerequest/',views.freelancer_completerequest),
    path('freelancer-viewproductdetail/',views.freelancer_viewproductdetail),
    path('freelancer-viewproducthistory/',views.freelancer_viewproducthistory),
    path('freelancer-viewchats/',views.freelancer_viewchats),
    path('freelancer-viewchatdetailed/',views.freelancer_viewchatdetailed),
    # path('newfreelancerchat/',views.new_freelancer_chat),
    #user
    path('user-register/',views.user_register),
    path('user-dashboard/',views.user_dashboard),
    path('user-viewcategories/',views.user_viewcategories),
    path('user-viewcatproducts/',views.user_viewcatproducts),
    path('user-addcart/',views.user_addcart),
    path('user-viewcart/',views.user_viewcart),
    path('user-removecartproduct/',views.user_removecartproduct),
    path('user-payment/',views.user_payment),
    path('user-viewhistory/',views.user_viewhistory),
    path('user-addreview/',views.user_addreview),
    path('user-updatereview/',views.user_updatereview),
    path('user-viewproductdetail/',views.user_viewproductdetail),
    path('user-viewfreelancers/',views.user_viewfreelancers),
    path('user-viewmoreworks/',views.user_viewmoreworks),
    path('user-makerequest/',views.user_makerequest),
    path('user-viewrequests/',views.user_viewrequests),
    path('user-payrequest/',views.user_payrequest),
    path('upi-form/',views.upi_form),
    path('credit-form/',views.credit_form),
    path('user-acceptrequire/',views.user_acceptrequire),
    path('user-rejectrequire/',views.user_rejectrequire),
    path('user-freelancerchat/',views.user_freelancerchat),
]
