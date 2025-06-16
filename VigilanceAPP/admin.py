from django.contrib import admin
from .models import Cliente, Rondas, Titulo, Comprovante, ConfiguracaoComprovante


admin.site.register(Cliente)
admin.site.register(Titulo)
admin.site.register(Comprovante)
admin.site.register(Rondas)
admin.site.register(ConfiguracaoComprovante)