from django.contrib import admin
from .models import Hospital,Vendor,Medicine
# Register your models here.
# h_iter=[]
# for h in Hospital.objects.all():
#     if h.is_verified==False:
#         h_iter.append(h)

# v_iter=[]
# for v in Vendor.objects.all():
#     if v.is_verified==False:
#         v_iter.append(h)

@admin.register(Hospital)
class AdminHospital(admin.ModelAdmin):
    fields=('hospital_name','hospital_document','is_verified')    


@admin.register(Vendor)
class AdminVendor(admin.ModelAdmin):
    fields=('vendor_name','vendor_verification_document','is_verified')

@admin.register(Medicine)
class MedAdmin(admin.ModelAdmin):
    pass