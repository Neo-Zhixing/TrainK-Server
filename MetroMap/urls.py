from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('stations', views.StationViewSet)
router.register('lines', views.LineViewSet)

urlpatterns = [
	re_path(r'^(?P<minX>-?\d+.?\d*):(?P<minY>-?\d+.?\d*):(?P<maxX>-?\d+.?\d*):(?P<maxY>-?\d+.?\d*)$', views.MapView.as_view()),
	path('', include(router.urls)),
	path('info', views.MapInfo)
]
