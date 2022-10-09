from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"demo", views.DemoViewSet, basename="demo")
router.register(r"infinite-demo", views.InfiniteDemoViewSet, basename="infinite-demo")

urlpatterns = [path("classic-demo/", views.demo_view)] + router.urls
