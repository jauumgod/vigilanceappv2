from django.contrib import admin
from .models import Cliente, Titulo, Comprovante, ConfiguracaoComprovante


admin.site.register(Cliente)
admin.site.register(Titulo)
admin.site.register(Comprovante)
admin.site.register(ConfiguracaoComprovante)