from django.contrib import admin
from .models import CuentaCobrar, CuentaCobrarCuota, CuentaCobrarPago

# Register your models here.

admin.site.register(CuentaCobrar)
admin.site.register(CuentaCobrarCuota)
admin.site.register(CuentaCobrarPago)
