from django.contrib.gis.db import models

# Create your models here.
class Activity(models.Model):
	tipo = models.TextField()
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
		return self.description

# class ActivityLine(models.Model):
# 	date = models.DateField()
# 	place = models.TextField()
# 	name = models.TextField()
# 	description = models.TextField()
# 	num_person = models.PositiveIntegerField()
# 	geom = models.LineStringField()
# 	instruments = models.TextField(null=True)
# 	focus = models.TextField(null=True)
# 	vos = models.TextField(null=True)
# 	result = models.TextField(null=True)

# 	def __str__(self):
# 		return self.description