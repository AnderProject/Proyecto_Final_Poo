from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Cliente , Ciudad
from .forms import ClienteForm, CiudadForm

#Vistas de la pagina Principal
 
class InicioListView(ListView):
    template_name = 'registration/login.html'
    context_object_name = 'inicio'

    def get_queryset(self):
        return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['title']= "Login"
        return context
    


    

class PrincipalListView(ListView):
    template_name = 'list.html'
    context_object_name = 'principal'

    def get_queryset(self):
        return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['title']= "---Pincipal---"
        context['titulo']= 'SECCION PRINCIPAL'
        return context



#Vitas del listado de Clientes 
class ClienteListView(ListView):
    model = Cliente
    template_name = 'Clientes/listado_cliente.html'
    context_object_name = 'clientes'
    paginate_by = 3
    query=""

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(nombre__icontains=query)
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "---AppClientes---"
        context['titulo']= 'LISTADO DE CLIENTES'
        return context
    
#Vistas de creacion de Clientes
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Clientes/cliente.html'
    success_url = reverse_lazy('clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "---AppClientes---"
        context['titulo']= 'SECCION DE REGISTAR CLIENTES'
        return context

#Vistas de modificar los datos de Clientes
class EditarClienteView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Clientes/cliente.html'
    success_url = reverse_lazy('clientes')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "AppClientes"
        context['titulo']= 'EDITAR LISTADO DEL CLIENTE'
        return context

#Vistas de eliminacion de Clientes  
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'Clientes/eliminar_cliente.html'
    success_url = reverse_lazy('clientes')




#Vistas de la Pagina Ciudad
class CiudadListView(ListView):
    template_name = 'ciudades/listado_ciudad.html'
    model = Ciudad
    context_object_name = 'ciudades'
    paginate_by= 3
    query= " "

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(descripcion__icontains=query)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "---AppCiudades---"
        context['titulo']= 'LISTADO DE CIUDADES'
        return context    

#Vistas de creacion de Clientes
class CiudadCreateView(CreateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'Ciudades/ciudad.html'
    success_url = reverse_lazy('ciudades')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "---AppCiudades---"
        context['titulo']= 'REGISTRAR CIUDADES'
        return context 

#Vistas de modificar los datos de Clientes
class CiudadUpdateView(UpdateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'Ciudades/ciudad.html'
    success_url = reverse_lazy('ciudades')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "---AppCiudades---"
        context['titulo']= 'EDITAR LISTADO CIUDAD'
        return context 



#Vistas de eliminacion de Clientes  
class CiudadDeleteView(DeleteView):
    model = Ciudad
    template_name = 'Ciudades/eliminar_ciudad.html'
    success_url = reverse_lazy('ciudades')



