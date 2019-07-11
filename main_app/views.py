from django.shortcuts import render,HttpResponse,redirect
from .forms import UserRegisterForm,HospitalRegisterForm,VendorRegisterForm,UserLoginForm,HospitalLoginForm,VendorLoginForm
from django.contrib.auth.models import User #Since no model forms are used, a new user object is to be created explicitly
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import Group#To use the groups functionality of django to differentiate between the user types
from .models import Normal_User,Hospital,Vendor,Hospital_To_Vendor_Order,User_To_Vendor_Order,Medicine,Items
from django.contrib.auth.decorators import login_required
from .forms import SearchForm,AddMedicineForm,UpdateForm

#-----------------------------------------------------------------------------------------------
#Function For Logout
#-----------------------------------------------------------------------------------------------
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
            if(form_data.cleaned_data['repeat']!=form_data.cleaned_data['Password']):
                return render(request,"NormalUserRegister.html",{'form':form},{'error':'Passwords Should Match'})
            new_user=User(username=form_data.cleaned_data['Username'],first_name=form_data.cleaned_data['First_Name'],last_name=form_data.cleaned_data['Last_Name'],email=form_data.cleaned_data['Email'])
            new_user.save()
            new_user.groups.add(1)
            new_user.set_password(form_data.cleaned_data['Password'])
            new_user.save()
            new_normal_user=Normal_User(phone_no=form_data.cleaned_data['Phone_Number'],auth_user=new_user)
            new_normal_user.save()            
            return redirect("u_h_login")
        else:
            return render(request,"NormalUserRegister.html",{'form':form},{'error':'Invalid Data Entered'})
    return render(request,"NormalUserRegister.html",{'form':form,'error':None})

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
            if(form_data.cleaned_data['repeat']!=form_data.cleaned_data['Password']):
                return render(request,"NormalUserRegister.html",{'form':form},{'error':'Passwords Should Match'})
            new_user=User(username=form_data.cleaned_data['Username'],email=form_data.cleaned_data['Email'])
            new_user.save()
            new_user.groups.add(2)
            new_user.set_password(form_data.cleaned_data['Password'])
            new_user.save()
            new_normal_user=Hospital(phone_no=form_data.cleaned_data['Phone_Number'],hospital_name=form_data.cleaned_data['HospitalName'],hospital_document=request.FILES['HospitalVerificationDocument'],auth_user=new_user,)
            new_normal_user.save()
            return redirect("u_h_login")
        else:
            return render(request,"NormalUserRegister.html",{'form':form},{'error':'Invalid Data Entered'})
    return render(request,"HospitalRegister.html",{'form':form,'error':None})
#-----------------------------------------------------------------------------------------------
#View for new vendor signup
#-----------------------------------------------------------------------------------------------

def register_new_vendor(request):
    form=VendorRegisterForm()
    if request.method=="POST":
        form_data=VendorRegisterForm(request.POST,request.FILES)
        #print(form_data)
        if form_data.is_valid():
            if(form_data.cleaned_data['repeat']!=form_data.cleaned_data['Password']):
                return render(request,"NormalUserRegister.html",{'form':form},{'error':'Passwords Should Match'})
            print("FAILED HERE")
            new_user=User(username=form_data.cleaned_data['Username'],email=form_data.cleaned_data['Email'])
            new_user.save()
            new_user.groups.add(3)
            new_user.set_password(form_data.cleaned_data['Password'])
            new_user.save()
            new_normal_user=Vendor(phone_no=form_data.cleaned_data['Phone_Number'],vendor_name=form_data.cleaned_data['VendorName'],vendor_verification_document=request.FILES['VendorVerificationDocument'],auth_user=new_user,)
            new_normal_user.save()      
            return redirect("v_login")      
        else:
            return render(request,"NormalUserRegister.html",{'form':form},{'error':'Invalid Data Entered'})
    return render(request,"HospitalRegister.html",{'form':form,'error':None})
#-----------------------------------------------------------------------------------------------
#View for user and hospital login
#-----------------------------------------------------------------------------------------------

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
#-----------------------------------------------------------------------------------------------
#View for vendor login
#-----------------------------------------------------------------------------------------------
    
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
#-----------------------------------------------------------------------------------------------
#View for Medicine Search
#-----------------------------------------------------------------------------------------------

@login_required(login_url="u_h_login")
def MedicineSearchView(request):
    if (request.user.groups.all())[0].id==3:
        return redirect("log_out") 
    if (request.user.groups.all())[0].id==2:
        for h in Hospital:
            if h.auth_user==request.user:
                if not h.is_verified:
                    return HttpResponse("Your Account Is Not Verified")
                break
    form=SearchForm()
    if request.method=="POST":
        if 'cart' in request.POST:
            req_id=request.POST.get('cart')
            quantity=request.POST.get(req_id)
            print(request.POST)
            return redirect("/add_to_cart/"+str(req_id)+"/"+str(quantity))
            
        search_query=SearchForm(request.POST)
        if search_query.is_valid():
            query=search_query.cleaned_data.get('search_query')
            all_results= Medicine.objects.filter(Medicine_name__icontains=query)
            print(all_results)
            if all_results==None:
                return HttpResponse("No Results")
            final_set=[]
            for res in all_results:
                if res.vendor_selling!=None:
                    print("HERE") 
                    print(res.vendor_selling.is_verified)
                    if res.vendor_selling.is_verified:
                        print("HERE ALSO")
                        final_set.append(res)
            print(final_set)        
            return render(request,'search_page.html',{'form':form,'results':final_set})
    return render(request,'search_page.html',{'form':form})     
#-----------------------------------------------------------------------------------------------
#View for Vendor's Inventory
#-----------------------------------------------------------------------------------------------

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
        if med.vendor_selling==vend:
            inv.append(med)        
    return render(request,"Inventory.html",{'inv':inv})
#-----------------------------------------------------------------------------------------------
#View for adding medicine to inventory
#-----------------------------------------------------------------------------------------------

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
#-----------------------------------------------------------------------------------------------
#View for updating medicine
#-----------------------------------------------------------------------------------------------

@login_required(login_url="v_login")
def vendor_update_medicine(request,id):
    med=Medicine.objects.get(id=id) 
    form=UpdateForm(initial={'Medicine_name':med.Medicine_name,'Medicine_price':med.Medicine_price,'Medicine_dosage':med.Medicine_dosage,'Medicine_type':med.Medicine_type,'total_quantity':med.total_quantity})
    if request.method=="POST":
        form_data=UpdateForm(request.POST)
        if form_data.is_valid():
            med.Medicine_name=form_data.cleaned_data.get('Medicine_name')
            med.Medicine_price=form_data.cleaned_data.get('Medicine_price')
            med.Medicine_dosage=form_data.cleaned_data.get('Medicine_dosage')
            med.Medicine_type=form_data.cleaned_data.get('Medicine_type')
            med.total_quantity=form_data.cleaned_data.get('total_quantity')
            med.save()
            return redirect('/vendor_page')
    return render(request,"UpdateMedicine.html",{'form':form})
#-----------------------------------------------------------------------------------------------
#View for deleting medicine
#-----------------------------------------------------------------------------------------------

@login_required(login_url="v_login")
def vendor_delete_medicine(request,id):
    Medicine.objects.get(id=id).delete()
    return redirect('/vendor_page')

#-----------------------------------------------------------------------------------------------
#View for adding medicine to cart
#-----------------------------------------------------------------------------------------------
@login_required(login_url="u_h_login")
def add_to_cart(request,id,quan):
    med=Medicine.objects.get(id=id)
    med_name=med.Medicine_name
    med_vendor=med.vendor_selling.vendor_name
    item=Items(vendor_name=med_vendor,medicine_name=med_name,quantity=quan)
    item.save()
    return redirect("m_search")

#-----------------------------------------------------------------------------------------------
#View to enable the user to view cart
#-----------------------------------------------------------------------------------------------
@login_required(login_url="u_h_login")
def view_cart(request):
    cart=Items.objects.all()
    notif_list=[]
    if request.method=="POST":
        ord=User_To_Vendor_Order()
            
    return render(request,'cart.html',{'items':cart})
    