from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from phone_field import PhoneFormField
from .models import Medicine

class UserRegisterForm(forms.Form):
    First_Name=forms.CharField(label="First Name",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'25','required':'True','autofocus':'True'}))
    Last_Name=forms.CharField(label="Last Name",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'25','required':'True'}))
    Username=forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Phone_Number=forms.CharField(label="Phone Number",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','pattern':'[0-9]{10}'}))
    Email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    repeat=forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    
class HospitalRegisterForm(forms.Form):
    HospitalName=forms.CharField(label="Hospital Name:",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','autofocus':'True'}))
    Username=forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Phone_Number=forms.CharField(label="Phone Number",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','pattern':'[0-9]{10}'}))
    Email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    repeat=forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    HospitalVerificationDocument=forms.FileField(label="Hospital Verification Document",allow_empty_file=False)

class VendorRegisterForm(forms.Form):
    VendorName=forms.CharField(label="Vendor Name",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','autofocus':'True'}))
    Username=forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Phone_Number=forms.CharField(label="Phone Number",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','pattern':'[0-9]{10}'}))
    Email=forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    repeat=forms.CharField(label="Repeat Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    VendorVerificationDocument=forms.FileField(label="Vendor License",allow_empty_file=False)
    
class UserLoginForm(forms.Form):
    Username=forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','autofocus':'True'}))
    Password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))

class HospitalLoginForm(forms.Form):
    HospitalName=forms.CharField(label="Hospital Name:",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','autofocus':'True'}))
    Username=forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))

class VendorLoginForm(forms.Form):
    VendorName=forms.CharField(label="Vendor Name",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','autofocus':'True'}))
    Username=forms.CharField(label="Username",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))
    Password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','maxlength':'30','required':'True'}))

class SearchForm(forms.Form):
    search_query=forms.CharField(label="Search",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','autofocus':'True'}))

class AddMedicineForm(forms.ModelForm):
    class Meta:
        model=Medicine
        fields = ('Medicine_price','Medicine_name','Medicine_dosage','Medicine_type','total_quantity')
        widgets={
            'Medicine_price':forms.NumberInput(attrs={'class':'form-control','autofocus':'true'}),
            'Medicine_name':forms.TextInput(attrs={'class':'form-control'}),
            'Medicine_dosage':forms.NumberInput(attrs={'class':'form-control'}),
            'Medicine_type':forms.Select(attrs={'class':'custom-select'}),
            'total_quantity':forms.NumberInput(attrs={'class':'form-control'}),
        }
        # exclude=['vendor_selling']
        
class UpdateForm(forms.Form):
    Medicine_name=forms.CharField(label="Medicine Name:",widget=forms.TextInput(attrs={'class':'form-control','maxlength':'30','required':'True','autofocus':'True','value':'{{med.Medicine_name}}'}))
    Medicine_price=forms.FloatField(label="Medicine Price",widget=forms.NumberInput(attrs={'class':'form-control','maxlength':'30','required':'True','value':'{{med.Medicine_price}}'}))
    Medicine_dosage=forms.IntegerField(label="Medicine Dosage",widget=forms.NumberInput(attrs={'class':'form-control','maxlength':'30','required':'True','value':'{{med.Medicine_dosage}}'}))
    types=(('Schedule 1','Schedule 1'),('Schedule 2','Schedule 2'),('Schedule 3','Schedule 3'),('Schedule 4','Schedule 4'),('Schedule 5','Schedule 5'))
    Medicine_type=forms.CharField(label="Medicine Type",widget=forms.Select(choices=types,attrs={'class':'form-control','maxlength':'30','required':'True','value':'{{med.Medicine_type}}'}))
    total_quantity=forms.IntegerField(label="Total Quantity",widget=forms.NumberInput(attrs={'class':'form-control','maxlength':'30','required':'True','value':'{{med.total_quantity}}'}))