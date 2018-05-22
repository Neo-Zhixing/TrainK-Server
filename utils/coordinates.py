class Position:
	x = 0
	y = 0

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __iter__(self):
		return iter([self.x, self.y])

	def inRect(self, rect):
		return rect.containsPoint(self)


class Size:
	width = 0
	height = 0


class Rect:
	origin = Position()
	size = Size()

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
