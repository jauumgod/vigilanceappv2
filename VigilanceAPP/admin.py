from django.contrib import admin
from .models import Cliente, Titulo, Comprovante


admin.site.register(Cliente)
admin.site.register(Titulo)
admin.site.register(Comprovante)