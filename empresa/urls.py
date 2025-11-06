from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EmpresaView

router = DefaultRouter()
router.register(r'empresas', EmpresaView)

urlpatterns = [
    path('', include(router.urls)),
]