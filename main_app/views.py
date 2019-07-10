from django.shortcuts import render,HttpResponse,redirect
from .forms import UserRegisterForm,HospitalRegisterForm,VendorRegisterForm,UserLoginForm,HospitalLoginForm,VendorLoginForm
from django.contrib.auth.models import User #Since no model forms are used, a new user object is to be created explicitly
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import Group#To use the groups functionality of django to differentiate between the user types
from .models import Normal_User,Hospital,Vendor,Hospital_To_Vendor_Order,User_To_Vendor_Order,Medicine
from django.contrib.auth.decorators import login_required
from .forms import SearchForm,AddMedicineForm
# Create your views here.

def all_logout(request):
    logout(request)
    return redirect("u_h_login")
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
                if not user:
                    return HttpResponse("Incorrect Credentials")
                if user and (user.groups.all())[0].id==1:
                    login(request,user)
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
                if not user:
                    return HttpResponse("INCORRECT CREDENTIALS")
                if user and (user.groups.all())[0].id==2:
                    for h in Hospital.objects.all():
                        if h.hospital_name==h_name and h.auth_user==user:
                            login(request,user)
                            return HttpResponse("SUCCESS")
                    return HttpResponse("INCORRECT CREDENTIALS")
                else:
                    return HttpResponse("INCORRECT CREDENTIALS")                    
    return render(request,"UserHospitalLogin.html",{'user_form':u_form,'hospital_form':h_form})
    
def vendor_login(request):
    v_form=VendorLoginForm()
    if request.method=="POST":
        form_data=VendorLoginForm(request.POST)
        if form_data.is_valid():
            u_name=form_data.cleaned_data.get("Username")
            pass_wd=form_data.cleaned_data.get("Password")
            v_name=form_data.cleaned_data.get("VendorName")
            user=authenticate(request,username=u_name,password=pass_wd)
            #print(user.groups.all())
            if not user:
                return HttpResponse("INCORRECT CREDENTIALS")
            if user and (user.groups.all())[0].id==3:
                for v in Vendor.objects.all():
                    if v.vendor_name==v_name and v.auth_user==user:
                        login(request,user)
                        return HttpResponse("SUCCESS")
                return HttpResponse("INCORRECT CREDENTIALS")
                    #login(request,user) 
            else:
                return HttpResponse("Incorrect Credentials")           
    return render(request,"vendor_login.html",{'form':v_form})

@login_required(login_url="u_h_login")
def MedicineSearchView(request):
    if (request.user.groups.all())[0].id==3:
        return redirect("log_out") 
    form=SearchForm()
    if request.method=="POST":
        a=1
    return render('search_page.html',{'form':form})     
    
@login_required(login_url="v_login")        
def VendorsView(request):
    if (request.user.groups.all())[0].id!=3:
        return redirect("log_out")
    all_medicine=Medicine.objects.all()
    vend=None
    for v in Vendor.objects.all():
        if v.auth_user==request.user:
            vend=v            
    inv=[]
    for med in all_medicine:
        if med.vendor_selling==v:
            inv.append(med)        
    return render(request,"Inventory.html",{'inv':inv})

@login_required(login_url="v_login")
def vendor_add_medicine(request):
    vend=None
    for v in Vendor.objects.all():
        if v.auth_user==request.user:
            vend=v 
            break   
    print(vend.vendor_name) 
    form=AddMedicineForm()
    if request.method=="POST":
        form_data=AddMedicineForm(request.POST)
        if form_data.is_valid():
            print('vend.id',vend.id)
            temp = form_data.save(commit=False)
            temp.vendor_selling=vend
            temp.save()
            print('form_data',temp.vendor_selling)
        else:
            print("FAILED")
    return render(request,"AddMedicine.html",{'form':form})

@login_required(login_url="v_login")
def vendor_update_medicine(request,id):
    return None

@login_required(login_url="v_login")
def vendor_delete_medicine(request,id):
    return None