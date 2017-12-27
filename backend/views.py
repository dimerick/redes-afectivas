from django.http import HttpResponse
from django.contrib.gis.geos import Point, LineString
from .models import Activity, ActivityLine


def index(request):
	#geom = Point(1, 1)
	with open('legion_2003.tsv','r') as tsv:
		for line in tsv:
			field = line.strip().split('\t')
			tipoh = str(field[0])
			dateh = str(field[1])
			placeh = str(field[2])
			nameh =	str(field[3])
			descriptionh = str(field[4])
			per_numh = str(field[5])
			instrumentsh = str(field[7])
			focush = str(field[8])					
			vosh =	str(field[9])
			resultsh = str(field[10])
			cords = field[6].split(',')
			#return HttpResponse(str(cords[1]))
			if tipoh == "A":
				geomh = Point(float(cords[0]),float(cords[1]))
				act = Activity(tipo = tipoh,date = dateh, place = placeh, name = nameh, description = descriptionh, num_person = per_numh, geom = geomh,
					instruments = instrumentsh, focus = focush, vos = vosh, result = resultsh)
			else:
				geomh = LineString(field[6])
				act = ActivityLine(tipo = tipoh,date = dateh, place = placeh, name = nameh, description = descriptionh, num_person = per_numh, geom = geomh,
					instruments = instrumentsh, focus = focush, vos = vosh, result = resultsh)
			act.save()

	return HttpResponse("Alers Rocking")





