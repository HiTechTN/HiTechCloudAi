from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, FileViewSet, CodeGenerationViewSet, SessionViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'files', FileViewSet)
router.register(r'generations', CodeGenerationViewSet)
router.register(r'sessions', SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
