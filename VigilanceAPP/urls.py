from django.urls import path, include
from .views import (
    ClientesCreateView,
    ConfiguracaoComprovanteViewSet,
    TitulosCreateView, 
    ComprovanteListView, 
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'clientes', ClientesCreateView, basename='clientes')
router.register(r'titulos', TitulosCreateView, basename='titulos')
router.register(r'comprovantes', ComprovanteListView, basename='comprovantes')
router.register(r'configuracao-comprovante', ConfiguracaoComprovanteViewSet)

urlpatterns = router.urls