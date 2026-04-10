from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import MineViewSet, custom_api_root

router = SimpleRouter()
router.register(r'mines', MineViewSet, basename='mine')

urlpatterns = [
    path('', custom_api_root, name='api-root'),
    path('', include(router.urls)),
]
