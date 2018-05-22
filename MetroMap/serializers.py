from rest_framework import serializers
from . import models


class NodeSerializer(serializers.ModelSerializer):
	position = serializers.ListField(
		child=serializers.DecimalField(max_digits=10, decimal_places=2),
		min_length=2,
		max_length=2
	)

	class Meta:
		model = models.Node
		fields = ('id', 'position')


class StationSerializer(NodeSerializer):
	class Meta(NodeSerializer.Meta):
		model = models.Station
		fields = NodeSerializer.Meta.fields + ('name', 'level')


class SegmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Segment
		fields = ('id', 'fromNode', 'toNode', 'length', 'shape')


class LineSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Line
		fields = ('id', 'name', 'attr', 'segment')
