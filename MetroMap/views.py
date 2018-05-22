from rest_framework import viewsets
from utils.permissions import IsAdminOrReadOnly

from . import models, serializers


class StationViewSet(viewsets.ModelViewSet):
	queryset = models.Station.objects.all()
	serializer_class = serializers.StationSerializer
	permission_classes = (IsAdminOrReadOnly, )
