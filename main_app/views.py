from django.shortcuts import render,HttpResponse
from .forms import UserRegisterForm,HospitalRegisterForm,VendorRegisterForm,UserLoginForm,HospitalLoginForm,VendorLoginForm
from django.contrib.auth.models import User #Since no model forms are used, a new user object is to be created explicitly
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import Group#To use the groups functionality of django to differentiate between the user types
from .models import Normal_User,Hospital,Vendor,Hospital_To_Vendor_Order,User_To_Vendor_Order
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

def user_and_hospital_login(request):
    u_form=UserLoginForm()
    h_form=HospitalLoginForm()
    if request.method=="POST":
        print(request.POST)
        if "form_for_user" in request.POST:
            form_data=UserLoginForm(request.POST)
            if form_data.is_valid():
                u_name=form_data.cleaned_data.get("Username")
                pass_wd=form_data.cleaned_data.get("Password")
                user=authenticate(request,username=u_name,password=pass_wd)
                #print(user.groups.all())
                if user and (user.groups.all())[0].id==1:
                    #login(request,user)
                    return HttpResponse("SUCCESS")
                else:
                    return HttpResponse("Incorrect Credentials")
        else:
            form_data=HospitalLoginForm(request.POST)
            if form_data.is_valid():
                u_name=form_data.cleaned_data.get("Username")
                pass_wd=form_data.cleaned_data.get("Password")
                h_name=form_data.cleaned_data.get("HospitalName")
                user=authenticate(request,username=u_name,password=pass_wd)
                #print(user.groups.all())
                if user and (user.groups.all())[0].id==2:
                    for h in Hospital.objects.all():
                        if h.hospital_name==h_name and h.auth_user==user:
                            return HttpResponse("SUCCESS")
                    print("THIS ERROR")
                        #login(request,user)
                    
                else:
                    return HttpResponse("Incorrect Credentials")           
    return render(request,"UserHospitalLogin.html",{'user_form':u_form,'hospital_form':h_form})
    
    

def MedicineSearchView(request):
    return None



    
    
    