from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_protect
from cmdb import models
# Create your views here.
#@csrf_protect
'''user_list=[
    {"user":"jack","pwd":"123"},
{"user":"tom","pwd":"456"},
]'''
def index(request):
    #return HttpResponse("hello world")
    if request.method=="POST":
        username=request.POST.get("username",None)
        password=request.POST.get("password",None)
        models.UserInfo.objects.create(user=username,pwd=password)
    user_list =models.UserInfo.objects.all()
    return render(request,"index.html",{"data":user_list})