from django.shortcuts import render
from .forms import UserRegisterForm,HospitalRegisterForm,VendorRegisterForm
from django.contrib.auth.models import User #Since no model forms are used, a new user object is to be created explicitly
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import Group#To use the groups functionality of django to differentiate between the user types
from .models import Normal_User,Hospital,Vendor
# Create your views here.

def user_login(request):
    return render(request,'user_login.html')
#-----------------------------------------------------------------------------------------------
#View for new user signup
#-----------------------------------------------------------------------------------------------
def register_new_user(request):
    form=UserRegisterForm()
    if request.method=="POST":
        form_data=UserRegisterForm(request.POST)
        #print(form_data)
        if form_data.is_valid():
            new_user=User(username=form_data.cleaned_data['Username'],first_name=form_data.cleaned_data['First_Name'],last_name=form_data.cleaned_data['Last_Name'],email=form_data.cleaned_data['Email'])
            new_user.save()
            new_user.groups.add(1)
            new_user.set_password(form_data.cleaned_data['Password'])
            new_user.save()
            new_normal_user=Normal_User(phone_no=form_data.cleaned_data['Phone_Number'],auth_user=new_user)
            new_normal_user.save()            
        else:
            print("ERROR OCCURS!!")
    return render(request,"NormalUserRegister.html",{'form':form})

#-----------------------------------------------------------------------------------------------
#View for new hospital signup
#-----------------------------------------------------------------------------------------------

def register_new_hospital(request): 
    form=HospitalRegisterForm()
    if request.method=="POST":
        form_data=HospitalRegisterForm(request.POST,request.FILES)
        #print(form_data)
        if form_data.is_valid():
            print("FAILED HERE")
            new_user=User(username=form_data.cleaned_data['Username'],email=form_data.cleaned_data['Email'])
            new_user.save()
            new_user.groups.add(2)
            new_user.set_password(form_data.cleaned_data['Password'])
            new_user.save()
            new_normal_user=Hospital(phone_no=form_data.cleaned_data['Phone_Number'],hospital_name=form_data.cleaned_data['HospitalName'],hospital_document=request.FILES['HospitalVerificationDocument'],auth_user=new_user,)
            new_normal_user.save()            
        else:
            print(form.errors)
            print("ERROR OCCURS!!")
    return render(request,"HospitalRegister.html",{'form':form})


def register_new_vendor(request):
    form=VendorRegisterForm()
    if request.method=="POST":
        form_data=VendorRegisterForm(request.POST,request.FILES)
        #print(form_data)
        if form_data.is_valid():
            print("FAILED HERE")
            new_user=User(username=form_data.cleaned_data['Username'],email=form_data.cleaned_data['Email'])
            new_user.save()
            new_user.groups.add(3)
            new_user.set_password(form_data.cleaned_data['Password'])
            new_user.save()
            new_normal_user=Vendor(phone_no=form_data.cleaned_data['Phone_Number'],vendor_name=form_data.cleaned_data['VendorName'],vendor_verification_document=request.FILES['VendorVerificationDocument'],auth_user=new_user,)
            new_normal_user.save()            
        else:
            print(form.errors)
            print("ERROR OCCURS!!")
    return render(request,"HospitalRegister.html",{'form':form})

def MedicineSearchView(request):
    return None



    
    
    