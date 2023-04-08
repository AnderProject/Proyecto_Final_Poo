from django.contrib.auth.models import User
from django.db import models
from Core.models import Cliente
from django.utils.timezone import now
from decimal import Decimal
# Create your models here.
    

#MODELS COBROS

estado_pago = (
    ('PA', 'Pagado'),
    ('PE', 'Pediente'),
)

class CuentaCobrar(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    fecha_credito = models.DateField(default=now)
    credito = models.DecimalField("credito",max_digits=10,decimal_places=2,default=Decimal(0))
    saldo = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal(0))
    numero_pagos = models.IntegerField(default=3)
    cuota = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    motivo = models.CharField(max_length=200)
    fecha_primer_pago = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=2, choices=estado_pago,default=estado_pago[0][0])

    class Meta:
        verbose_name = "Cuenta por Cobrar"
        verbose_name_plural = "Cuentas por Cobrar"

    def __str__(self):
        return '{}'.format(self.credito)


class CuentaCobrarCuota(models.Model):
    ESTADO_PENDIENTE = 0
    ESTADO_PAGADO = 1
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
    ]
    cuenta_cobrar = models.ForeignKey(CuentaCobrar, on_delete=models.CASCADE)
    fecha_pagar = models.DateField('Fecha Pagar',blank=True, null=True)
    cuota = models.DecimalField("Couta", max_digits=10, decimal_places=2)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    
    class Meta:
        verbose_name = "Cuenta x Cobrar detalle"
        verbose_name_plural = "Cuentas x Cobrar detalle"

    def __str__(self):
        return '{}'.format(self.fecha_pagar)


class CuentaCobrarPago(models.Model):
    cuenta_cobrar_cuota = models.ForeignKey(CuentaCobrarCuota, on_delete=models.CASCADE)
    fecha_pago = models.DateField('Fecha Pago',default=now)
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Cuenta x Cobrar Pago"
        verbose_name_plural = "Cuentas x Cobrar Pago"

    def __str__(self):
        return '{}'.format(self.fecha_pago)