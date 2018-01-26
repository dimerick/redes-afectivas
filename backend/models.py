from django.contrib.gis.db import models
from django.contrib.gis.geos import WKTWriter

# Create your models here.
class Activity(models.Model):
	date = models.DateField()
	place = models.TextField()
	name = models.TextField()
	description = models.TextField()
	num_person = models.PositiveIntegerField()
	geom = models.GeometryField()
	instruments = models.TextField(null=True)
	focus = models.TextField(null=True)
	vos = models.TextField(null=True)
	result = models.TextField(null=True)

	def __str__(self):
		wkt_w = WKTWriter()
		return str(self.id)+" | "+str(self.date)+" | "+self.place+" | "+self.description+" | "+str(wkt_w.write(self.geom))

# class Activity(models.Model):
# 	geom = models.GeometryField()

