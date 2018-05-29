from enum import Enum, unique
from utils import ModelFieldEnum, coordinates

from django.db import models
from django.urls import reverse
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

	@property
	def position(self):
		return coordinates.Point(x=self.positionX, y=self.positionY)

	@position.setter
	def position(self, value):
		self.positionX = value.x
		self.positionY = value.y

	def __str__(self):
		if hasattr(self, 'station'):
			return self.station.__str__()
		return f'{self.id} - ({self.positionX:.2f}, {self.positionY:.2f})'


class Station(Node):
	name = models.CharField(max_length=30)

	@unique
	class Level(int, ModelFieldEnum, Enum):
		Minor = 0
		Major = 1
		Interchange = 2
		Intercity = 3

	level = models.IntegerField(choices=Level.choices(), default=Level.Minor)

	def __str__(self):
		return f'{self.id} - {self.name} ({self.positionX:.2f}, {self.positionY:.2f})'

	def get_absolute_url(self):
		return reverse('station-detail', args=[str(self.id)])


class Line(models.Model):
	name = models.CharField(max_length=30)
	attr = JSONField()

	def __str__(self):
		return self.name


class Segment(models.Model):
	fromNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='_origin_segment')
	toNode = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='_destination_segment')
	length = models.DecimalField(max_digits=3, decimal_places=2, default=1)  # In kilometers
	line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='segments')

	@unique
	class Shape(int, ModelFieldEnum, Enum):
		Square = 0
		Triangle = 1
		Curve = 2
		Parallel = 3
		Straight = 4

	shape = models.IntegerField(choices=Shape.choices())
