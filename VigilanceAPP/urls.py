from django.urls import path, include

from VigilanceAPP.serializers import UserAdminViewSet
from .views import (
    ClientesCreateView,
    ConfiguracaoComprovanteViewSet,
    EmpresaCreateView,
    LogoComprovanteView,
    RondasCreateView,
    TitulosCreateView, 
    ComprovanteCreateView,
    ComprovanteListView,
    UltimaConfiguracaoComprovante, gerar_titulos, enderecos_unicos, dashboard_data
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  CustomTokenObtainPairView, UserListCreateView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'clientes', ClientesCreateView, basename='clientes')
router.register(r'titulos', TitulosCreateView, basename='titulos')
router.register(r'comprovantes', ComprovanteCreateView, basename='comprovantes')
router.register(r'configuracao-comprovante', ConfiguracaoComprovanteViewSet, basename='configuracao-comprovante')
router.register(r'rondas', RondasCreateView, basename='rondas')
router.register(r'admin/users', UserAdminViewSet, basename='admin-users')
router.register(r'empresas', EmpresaCreateView, basename='empresas')

urlpatterns = router.urls

urlpatterns = [
    path('gerar-titulos/', gerar_titulos, name='gerar_titulos'),
    path('enderecos-unicos/',enderecos_unicos, name='enderecos-unicos'),
    path('logo-comprovante/', LogoComprovanteView.as_view(), name='logo-comprovante'),
    path('comprovantes/criar/', ComprovanteListView.as_view(), name='criar_comprovante'),
    
    path('dashboard/', dashboard_data, name='dashboard-data'),
    path('configuracao-comprovante/ultima/', UltimaConfiguracaoComprovante.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]