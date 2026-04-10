from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MineViewSet

router = DefaultRouter()
router.register(r'mines', MineViewSet, basename='mine')

urlpatterns = [
    path('', include(router.urls)),
]
