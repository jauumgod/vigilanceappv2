from django.contrib import admin
from .models import Cliente, Empresa, Rondas, Titulo, Comprovante, ConfiguracaoComprovante, UserEmpresa


admin.site.register(Cliente)
admin.site.register(Titulo)
admin.site.register(Comprovante)
admin.site.register(Rondas)
admin.site.register(ConfiguracaoComprovante)
admin.site.register(Empresa)
admin.site.register(UserEmpresa)