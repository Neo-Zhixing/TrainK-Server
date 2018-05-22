from django.contrib import admin
from . import models


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
	pass
