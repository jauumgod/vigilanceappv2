from django.urls import path, include

from VigilanceAPP.serializers import UserAdminViewSet
from .views import (
    ClientesCreateView,
    ConfiguracaoComprovanteViewSet,
    LogoComprovanteView,
    RondasCreateView,
    TitulosCreateView, 
    ComprovanteCreateView,
    ComprovanteListView, gerar_titulos, enderecos_unicos, dashboard_data
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'clientes', ClientesCreateView, basename='clientes')
router.register(r'titulos', TitulosCreateView, basename='titulos')
router.register(r'comprovantes', ComprovanteCreateView, basename='comprovantes')
router.register(r'configuracao-comprovante', ConfiguracaoComprovanteViewSet)
router.register(r'rondas', RondasCreateView, basename='rondas')
router.register(r'admin/users', UserAdminViewSet, basename='admin-users')

urlpatterns = router.urls

urlpatterns = [
    path('gerar-titulos/', gerar_titulos, name='gerar_titulos'),
    path('enderecos-unicos/',enderecos_unicos, name='enderecos-unicos'),
    path('logo-comprovante/', LogoComprovanteView.as_view(), name='logo-comprovante'),
    path('comprovantes/criar/', ComprovanteListView.as_view(), name='criar_comprovante'),
    # path('comprovantes/', ComprovanteListView.as_view(), name='criar_comprovante'),
    path('dashboard/', dashboard_data, name='dashboard-data'),
    path('', include(router.urls)),
]