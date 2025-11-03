from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AcionistaView

router = DefaultRouter()
router.register(r'acionistas', AcionistaView)

urlpatterns = [
    path('', include(router.urls)),
]
