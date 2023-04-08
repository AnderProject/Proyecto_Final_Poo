from django.shortcuts import render
from django.views.generic import ListView
from .models import CuentaCobrar, CuentaCobrarPago, CuentaCobrarCuota, CuentaCobrarPago
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView , UpdateView, DeleteView
from .forms import CuentaCobrarForm
import json
from django.http import JsonResponse, HttpResponseRedirect
from datetime import datetime
from django.shortcuts import get_object_or_404



# Create your views here.

#Cuenta_x_Cobrar

class CuentaCobrarListView(ListView):
    model = CuentaCobrar
    template_name = 'cuenta_x_cobrar/listado_cuenta_cobrar.html'
    context_object_name = 'cuentas_cobrar'
    paginate_by = 3
    
    def get_queryset(self):
        return super().get_queryset().order_by('cliente__nombre')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "AppCobros"
        context['titulo']= 'GESTION DE CREDITOS DE COBROS'
        return context
    


    
class CuentaCobrarCreateView(CreateView):
    model = CuentaCobrar
    form_class = CuentaCobrarForm
    template_name = 'cuenta_x_cobrar/cuenta_cobrar.html'
    success_url = reverse_lazy('cuenta')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']= "---AppCreditos---"
        context['titulo']= 'REGISTRO DE CREDITOS'
        return context 

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            cuenta_id = self.kwargs.get('pk')

            # código agregado
            if cuenta_id:
                cuenta = get_object_or_404(CuentaCobrar, id=cuenta_id)
                cuenta.fecha_credito = datetime.strptime(data['fecha_credito'], '%Y-%m-%d').date()
                cuenta.credito = data['credito']
                cuenta.cliente_id = data['cliente']
                cuenta.numero_pagos = data['numero_pagos']
                cuenta.cuota = data['cuota']
                cuenta.fecha_primer_pago = datetime.strptime(data['fecha_primer_pago'], '%Y-%m-%d').date()
                cuenta.saldo = data['saldo']
                cuenta.motivo = data['motivo']
                cuenta.save()

                # Eliminar pagos existentes
                cuenta.cuentacobrarcuota_set.all().delete()

            else:
                cuenta = CuentaCobrar(
                    fecha_credito=datetime.strptime(data['fecha_credito'], '%Y-%m-%d').date(),
                    credito=data['credito'],
                    cliente_id=data['cliente'],
                    numero_pagos=data['numero_pagos'],
                    cuota=data['cuota'],
                    fecha_primer_pago=datetime.strptime(data['fecha_primer_pago'], '%Y-%m-%d').date(),
                    saldo=data['saldo'],
                    motivo=data['motivo']
                )
                cuenta.save()

            # Crear pagos
            pagos_data = data['pagos']
            cuenta_pagada = True  # bandera para verificar si todas las cuotas han sido pagadas
            for i, pago_data in enumerate(pagos_data):
                cuota = CuentaCobrarCuota(
                    cuenta_cobrar=cuenta,
                    fecha_pagar = datetime.strptime(pago_data['fecha_pago'], '%d/%m/%Y').date(),
                    cuota=pago_data['cuota'],
                    estado=0  # cambiar el valor por defecto a 0 (pendiente)
                )
                cuota.save()

                # Crear pagos realizados
                if pago_data['pagado']:
                    pago = CuentaCobrarPago(
                        cuenta_cobrar_cuota=cuota,
                        fecha_pago=datetime.now(),
                        valor=pago_data['cuota']
                    )
                    pago.save()
                else:
                    cuenta_pagada = False  # si hay alguna cuota pendiente, la cuenta no está pagada

            # si todas las cuotas han sido pagadas, cambiar el estado de la cuenta a "pagado"
            if cuenta_pagada:
                cuenta.estado = 1
                cuenta.save()
            else:
                cuenta.estado = 0  # si hay alguna cuota pendiente, la cuenta está "pendiente"
                cuenta.save()

            return JsonResponse({'status': 'success'})
        else:
            return super().post(request, *args, **kwargs)
        
        
class EditarCuentaView(UpdateView):
    model = CuentaCobrar
    form_class = CuentaCobrarForm
    template_name = 'cuenta_x_cobrar/cuenta_cobrar.html'
    success_url = reverse_lazy('cuenta')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cuenta_id = self.kwargs.get('pk')
        cuenta = get_object_or_404(CuentaCobrar, id=cuenta_id)
        cuotas = cuenta.cuentacobrarcuota_set.all()
        context['cuotas'] = cuotas
        context['title']= "AppCobros"
        context['titulo']= 'GESTION DE CREDITOS DE COBROS'
        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # procesar solicitud ajax para actualizar pagos
            data = json.loads(request.body)
            cuenta_id = self.kwargs.get('pk')
            cuenta = get_object_or_404(CuentaCobrar, id=cuenta_id)
            cuotas = cuenta.cuentacobrarcuota_set.all()

            # actualizar pagos
            for cuota in cuotas:
                pago_id = data.get(f'pago_{cuota.id}')
                if pago_id:
                    pago = get_object_or_404(CuentaCobrarPago, id=pago_id)
                    pago.fecha_pago = datetime.now().date()
                    pago.save()

            # verificar si todas las cuotas están pagadas
            cuenta_pagada = all(cuota.pagado for cuota in cuotas)

            # leer los datos del formulario de la solicitud HTTP
            fecha_credito = data.get('fecha_credito')
            credito = data.get('credito')
            cliente = data.get('cliente')
            numero_pagos = data.get('numero_pagos')
            cuota = data.get('cuota')
            fecha_primer_pago = data.get('fecha_primer_pago')
            saldo = data.get('saldo')
            motivo = data.get('motivo')
            pagos = data.get('pagos')

            # crear el formulario y actualizar la instancia del modelo
            form = self.form_class(data=request.POST, instance=cuenta)
            if form.is_valid():
                cuenta = form.save(commit=False)
                cuenta.fecha_credito = fecha_credito
                cuenta.credito = credito
                cuenta.cliente = cliente
                cuenta.numero_pagos = numero_pagos
                cuenta.cuota = cuota
                cuenta.fecha_primer_pago = fecha_primer_pago
                cuenta.saldo = saldo
                cuenta.motivo = motivo
                cuenta.estado = CuentaCobrar.ESTADO_PAGADA if cuenta_pagada else CuentaCobrar.ESTADO_PENDIENTE
                cuenta.save()

                for pago_data in pagos:
                    pago_id = pago_data.get('id')
                    if pago_id:
                        pago = get_object_or_404(CuentaCobrarPago, id=pago_id)
                        pago.fecha_pago = datetime.strptime(pago_data.get('fecha_pago'), '%d/%m/%Y').date()
                        pago.cuota = pago_data.get('cuota')
                        pago.pagado = pago_data.get('pagado')
                        pago.save()

                return JsonResponse({'status': 'success'})
            else:
                form = self.form_class(data=request.POST, instance=self.get_object())
                if form.is_valid():
                    cuenta = form.save(commit=False)
                    cuenta.save()

                    for cuota_data in request.POST.getlist('cuota_data[]'):
                        cuota_id, estado = cuota_data.split(',')
                        cuota = get_object_or_404(CuentaCobrarCuota, id=int(cuota_id))
                        cuota.estado = int(estado)
                        cuota.save()

                    return HttpResponseRedirect(self.success_url)
                else:
                    context = self.get_context_data(**kwargs)
                    context['form'] = form
                    return self.render_to_response(context)
                
class CuentaDeleteView(DeleteView):
    model = CuentaCobrar
    template_name = 'cuenta_x_cobrar/eliminar_cuenta.html'
    success_url = reverse_lazy('cuenta')