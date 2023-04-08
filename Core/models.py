from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User


# MODELS BASE

genero = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)

class Ciudad(models.Model):
    descripcion = models.CharField("Descripcion",max_length=50)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)

    def __str__(self):
        return f'{self.id} - {self.descripcion}'

class Cliente(models.Model):
    nombre = models.CharField("Cliente",max_length=50)
    cedula = models.CharField("Cedula",max_length=10)
    foto = models.FileField(upload_to='clientes/fotos', null=True, blank=True)
    email = models.EmailField("Correo")
    ciudad = models.ForeignKey(Ciudad,on_delete=models.PROTECT,null=True,blank=True)
    sexo = models.CharField("Sexo", choices=genero, default=genero[0][0], max_length=1)
    cupo = models.DecimalField("Cupo",max_digits=10,decimal_places=2,default=Decimal(0))
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)
    
    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.foto:
            return '{}{}'.format(settings.MEDIA_URL, self.foto)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.jpg')

    
