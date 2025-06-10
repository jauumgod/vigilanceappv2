from django.urls import path, include
from .views import (
    ClientesCreateView,
    ConfiguracaoComprovanteViewSet,
    LogoComprovanteView,
    TitulosCreateView, 
    ComprovanteCreateView,
    ComprovanteListView, gerar_titulos, enderecos_unicos
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'clientes', ClientesCreateView, basename='clientes')
router.register(r'titulos', TitulosCreateView, basename='titulos')
router.register(r'comprovantes', ComprovanteCreateView, basename='comprovantes')
router.register(r'configuracao-comprovante', ConfiguracaoComprovanteViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('gerar-titulos/', gerar_titulos, name='gerar_titulos'),
    path('enderecos-unicos/',enderecos_unicos, name='enderecos-unicos'),
    path('logo-comprovante/', LogoComprovanteView.as_view(), name='logo-comprovante'),
    path('comprovantes/criar/', ComprovanteListView.as_view(), name='criar_comprovante'),
    path('comprovantes/', ComprovanteListView.as_view(), name='criar_comprovante'),
    path('', include(router.urls)),
]