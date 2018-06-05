from django.db.models import Q, Max, Min
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.permissions import IsAdminOrReadOnly

from . import models, serializers
from drf_multiple_model.views import ObjectMultipleModelAPIView


@api_view()
def MapInfo(request):
	return Response({
		'frame': models.Node.objects.all().aggregate(
			minX=Min('positionX'),
			minY=Min('positionY'),
			maxX=Max('positionX'),
			maxY=Max('positionY')
		),
		'spacing': 100,
		'styles': 'kkkk',
		'title': 'A Metro Map',
		'cornerRadius': 15,
	})


class StationViewSet(viewsets.ModelViewSet):
	queryset = models.Station.objects.all()
	serializer_class = serializers.StationSerializer
	permission_classes = (IsAdminOrReadOnly, )

	def get_queryset(self):
		queryset = super().get_queryset()
		try:
			within = self.request.query_params['within']
			minX, minY, maxX, maxY = tuple(within.split('-', 4))
			queryset = queryset.filter(
				positionX__gte=minX,
				positionX__lte=maxX,
				positionY__gte=minY,
				positionY__lte=maxY
			)
		except Exception:
			pass
		return queryset


class LineViewSet(viewsets.ModelViewSet):
	queryset = models.Line.objects.all()
	serializer_class = serializers.LineDetailSerializer
	permissions = (IsAdminOrReadOnly, )


class MapView(ObjectMultipleModelAPIView):

	def get_querylist(self):
		self.nodeQueryset = models.Node.objects.filter(
			positionX__gte=self.kwargs['minX'],
			positionX__lte=self.kwargs['maxX'],
			positionY__gte=self.kwargs['minY'],
			positionY__lte=self.kwargs['maxY']
		)
		self.segmentQueryset = models.Segment.objects.filter(
			Q(fromNode__in=self.nodeQueryset) | Q(toNode__in=self.nodeQueryset)
		).select_related('line')
		return [
			{
				'queryset': self.nodeQueryset.filter(station__isnull=True),
				'serializer_class': serializers.NodeSerializer,
				'label': 'nodes'
			},
			{
				'queryset': map(
					lambda node: node.station,
					self.nodeQueryset.filter(station__isnull=False).select_related('station')
				),
				'serializer_class': serializers.StationSerializer,
				'label': 'stations'
			},
			{
				'queryset': self.segmentQueryset,
				'serializer_class': serializers.SegmentSerializer,
				'label': 'segments'
			},
			{
				'queryset': set(map(
					lambda segment: segment.line,
					self.segmentQueryset
				)),
				'serializer_class': serializers.LineSerializer,
				'label': 'lines'
			}
		]
