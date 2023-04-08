"""Cuentas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Core.views import ClienteListView, InicioListView, EditarClienteView, ClienteDeleteView, ClienteCreateView, PrincipalListView
from django.contrib.staticfiles.urls import static
from Core.views import CiudadListView, CiudadCreateView, CiudadUpdateView, CiudadDeleteView
from django.conf import settings
from cobros.views import CuentaCobrarListView, CuentaCobrarCreateView, EditarCuentaView, CuentaDeleteView


from login import views
from django.contrib.auth import views as auth_views

app_name = 'login'

urlpatterns = [
    path('admin/', admin.site.urls),

        # URLS DE CLIENTES
    path('login/', InicioListView.as_view(), name='inicio'),
    path('principal/', PrincipalListView.as_view(), name='principal'),
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('crear_cliente/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('editar_cliente/<int:pk>/', EditarClienteView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),



        #URLS DE CIUDADES
    path('ciudades/', CiudadListView.as_view(), name='ciudades'),
    path('crear_ciudad/', CiudadCreateView.as_view(), name='crear_ciudad'),
    path('editar_ciudad/<int:pk>/', CiudadUpdateView.as_view(), name='editar_ciudad'),
    path('eliminar_ciudad/<int:pk>/', CiudadDeleteView.as_view(), name='eliminar_ciudad'),



            #URLS DE COBROS
    path('cuenta/', CuentaCobrarListView.as_view(), name='cuenta'),
    path('crear_cuenta/', CuentaCobrarCreateView.as_view(), name='crear_cuentas_cobrar'),
    path('editar_cuenta/<int:pk>/', EditarCuentaView.as_view(), name='editar_cuenta'),
    path('eliminar_cuenta/<int:pk>/', CuentaDeleteView.as_view(), name='eliminar_cuenta'),


    #Login

    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', views.dashboard, name='dashboard'),











]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
