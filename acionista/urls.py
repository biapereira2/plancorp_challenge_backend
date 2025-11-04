from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AcionistaView, ParticipacaoViewSet


router = DefaultRouter()
router.register(r'acionistas', AcionistaView)
router.register(r'participacoes', ParticipacaoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
