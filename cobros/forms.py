from django import forms
from django.forms import ModelForm
from .models import CuentaCobrar, CuentaCobrarCuota, CuentaCobrarPago
from datetime import datetime


# CuentaCobrarForm
class CuentaCobrarForm(ModelForm):
    class Meta:
        model = CuentaCobrar
        fields = ('cliente', 'fecha_credito', 'credito', 'saldo', 'numero_pagos', 'cuota', 'motivo', 'fecha_primer_pago', 'estado')
        labels= {'motivo' : 'Referencia'}

        widgets = {
            'fecha_credito': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs= {'class': 'form-control', 'value': datetime.now().strftime('%Y-%m-%d'),'type':'date'}
            ),

            'fecha_primer_pago': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs= {'class': 'form-control', 'value': datetime.now().strftime('%Y-%m-%d'),'type':'date'}
            ),

            'cuota' : forms.TextInput(
            attrs={'class': 'form-control', 'readonly': 'readonly'}
            ),
        }


# CuentaCobrarCuotaForm
class CuentaCobrarCuotaForm(ModelForm):
    class Meta:
        model = CuentaCobrarCuota
        fields = ('cuenta_cobrar', 'fecha_pagar', 'cuota', 'estado')

# CuentaCobrarPagoForm
class CuentaCobrarPagoForm(ModelForm):
    class Meta:
        model = CuentaCobrarPago
        fields = ('cuenta_cobrar_cuota', 'fecha_pago', 'valor') 