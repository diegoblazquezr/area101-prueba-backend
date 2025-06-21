from rest_framework.routers import DefaultRouter
from .views import SessionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'sessions', SessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
]