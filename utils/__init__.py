class ModelFieldEnum:
	@classmethod
	def choices(cls):
		return [(member.value, name) for name, member in cls.__members__.items()]
