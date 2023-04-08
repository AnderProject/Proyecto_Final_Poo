from django.contrib import admin
from .models import Cliente, Ciudad

admin.site.register(Ciudad)
admin.site.register(Cliente)