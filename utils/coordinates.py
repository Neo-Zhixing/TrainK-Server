class Point:
	x = 0
	y = 0

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __str__(self):
		return "(%f, %f)" % (self.x, self.y)

	def inRect(self, rect):
		return rect.containsPoint(self)


class Size:
	width = 0
	height = 0

	def __init__(self, width=0, height=0):
		self.width = width
		self.height = height

	def __str__(self):
		return "%fx%f" % (self.width, self.height)


class Rect:
	origin = Point()
	size = Size()

	def __init__(self, **kwargs):
		if 'origin' in kwargs and 'size' in kwargs:
			self.origin = kwargs['origin']
			self.size = kwargs['size']
		elif 'x' in kwargs and 'y' in kwargs and \
			'width' in kwargs and 'height' in kwargs:
			self.origin = Point(x=kwargs['x'], y=kwargs['y'])
			self.size = Size(width=kwargs['width'], height=kwargs['height'])
		elif 'minX' in kwargs and 'minY' in kwargs and \
			'maxX' in kwargs and 'maxY' in kwargs:
			self.origin = Point(x=kwargs['minX'], y=kwargs['minY'])
			self.size = Size(width=kwargs['maxX'] - self.origin.x, height=kwargs['maxY'] - self.origin.y)
		else:
			self.origin = Point()
			self.size = Size()

	def __str__(self):
		return "%s, %s" % (self.origin.__str__(), self.size.__str__())

	@property
	def minX(self):
		return self.origin.x

	@minX.setter
	def minX(self, value):
		self.size.width += self.origin.x - value
		self.origin.x = value

	@property
	def minY(self):
		return self.origin.y

	@minY.setter
	def minY(self, value):
		self.size.height += self.origin.y - value
		self.origin.y = value

	@property
	def maxX(self):
		return self.origin.x + self.size.width

	@maxX.setter
	def maxX(self, value):
		self.size.width = value - self.origin.x

	@property
	def maxY(self):
		return self.origin.y + self.size.width

	@maxY.setter
	def maxY(self, value):
		self.size.height = value - self.origin.y

	def containsPoint(self, point):
		return point.x >= self.minX and point.x <= self.maxX and \
			point.y >= self.minY and point.y <= self.maxY
