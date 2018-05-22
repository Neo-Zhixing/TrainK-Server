from enum import Enum, unique
from utils import ModelFieldEnum

from django.db import models
from django.contrib.postgres.fields import JSONField


class Node(models.Model):
	positionX = models.DecimalField(max_digits=10, decimal_places=2)
	positionY = models.DecimalField(max_digits=10, decimal_places=2)

	@property
	def segments(self):
		return self._origin_segment.union(self._destination_segment)

	@property
	def lines(self):
		return self.segments.lines


class Station(Node):
	name = models.CharField(max_length=30)

	@unique
	class Level(int, ModelFieldEnum, Enum):
		Minor = 0
		Major = 1
		Interchange = 2
		Intercity = 3

	level = models.IntegerField(choices=Level.choices(), default=Level.Minor)


class Segment(models.Model):
	fromNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='_origin_segment')
	toNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='_destination_segment')
	length = models.DecimalField(max_digits=3, decimal_places=2, default=1)  # In kilometers

	@unique
	class Shape(int, ModelFieldEnum, Enum):
		Square = 0
		Triangle = 1
		Curve = 2
		Parallel = 3
		Straight = 4

	shape = models.IntegerField(choices=Shape.choices())


class Line(models.Model):
	name = models.CharField(max_length=30)
	attr = JSONField()
	segments = models.ManyToManyField(Segment, related_name='lines')
