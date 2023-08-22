from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Login)
admin.site.register(FreelancerReg)
admin.site.register(Cart)
admin.site.register(UserReg)
admin.site.register(Product)
admin.site.register(FreelancerCategory)
admin.site.register(Category)
admin.site.register(RequestProduct)
admin.site.register(Chat)
admin.site.register(Feedback)