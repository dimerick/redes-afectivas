from django.http import HttpResponse
from django.contrib.gis.geos import Point, LineString
from .models import Activity
import ast

# locations = cod_des-cod_or	cod_des-cod_or1,cod_or2,cod_or3

def index(request):	
	# t = "(-75.574974, 6.307394),(-74.970628, 5.844590)"
	# ls = LineString(ast.literal_eval(t))
	# return HttpResponse(str(ls))
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
			#return HttpResponse(str(cords[1]))
			if tipoh == "p":
				geomh = Point(ast.literal_eval(field[6].strip()))
			else:
				geomh = LineString(ast.literal_eval(field[6].strip()))
			act = Activity(tipo = tipoh,date = dateh, place = placeh, name = nameh, description = descriptionh, num_person = per_numh, geom = geomh,
					instruments = instrumentsh, focus = focush, vos = vosh, result = resultsh)
			
			act.save()

	return HttpResponse("Alers Rocking")





