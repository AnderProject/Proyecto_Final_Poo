from django import forms
from .models import Ciudad, Cliente

# CiudadForm
class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['descripcion', 'estado']

# ClienteForm
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            'nombre': 'Nombre del cliente',
            'cedula': 'Cédula',
            'foto': 'Foto del cliente',
            'email': 'Correo electrónico',
            'ciudad': 'Ciudad',
            'sexo': 'Sexo',
            'cupo': 'Cupo',
            'estado': 'Estado'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'cupo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
