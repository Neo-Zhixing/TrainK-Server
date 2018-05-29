from rest_framework import serializers
from . import models


class PointSerializer(serializers.Serializer):
	x = serializers.DecimalField(max_digits=10, decimal_places=2)
	y = serializers.DecimalField(max_digits=10, decimal_places=2)


class NodeSerializer(serializers.ModelSerializer):
	position = PointSerializer()

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
		fields = ('id', 'from', 'to', 'length', 'shape', 'line')
		extra_kwargs = {
			'from': {'source': 'fromNode'},
			'to': {'source': 'toNode'}
		}


class SegmentDetailSerializer(SegmentSerializer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['from'] = serializers.SerializerMethodField(method_name='get_from_node')
		self.fields['to'] = serializers.SerializerMethodField(method_name='get_to_node')

	def get_from_node(self, instance):
		node = getattr(instance.fromNode, 'station', instance.fromNode)
		if hasattr(node, 'station'):
			return StationSerializer(node.station).data
		return NodeSerializer(node).data

	def get_to_node(self, instance):
		node = getattr(instance.toNode, 'station', instance.toNode)
		if hasattr(node, 'station'):
			return StationSerializer(node.station).data
		return NodeSerializer(node).data

	class Meta(SegmentSerializer.Meta):
		fields = ('id', 'fromNode', 'toNode', 'length', 'shape')
		extra_kwargs = {
			'fromNode': {'write_only': True},
			'toNode': {'write_only': True}
		}


class LineSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Line
		fields = ('id', 'name', 'attr')


class LineDetailSerializer(serializers.ModelSerializer):
	segments = SegmentDetailSerializer(many=True)

	class Meta(LineSerializer.Meta):
		fields = ('id', 'name', 'attr', 'segments')

	def _update_segments(self, line, data):
		segments_to_delete = models.Segment.objects.filter(line=line)
		for segment in data:
			segments_to_delete = segments_to_delete.exclude(fromNode=segment['fromNode'], toNode=segment['toNode'])
			models.Segment.objects.update_or_create(defaults=segment, line=line, fromNode=segment['fromNode'], toNode=segment['toNode'])
		segments_to_delete.delete()

	def create(self, validated_data):
		segments = validated_data.pop('segments')
		line = models.Line(**validated_data)
		line.save()
		self._update_segments(line, segments)
		return line

	def update(self, line, validated_data):
		if 'segments' in validated_data:
			segments = validated_data.pop('segments')
			self._update_segments(line, segments)
		for key, value in validated_data.items():
			setattr(line, key, value)
		line.save()
		return line
