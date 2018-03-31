from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.geos import GEOSGeometry, LineString
from .models import Activity
import ast
from django.shortcuts import render
from .forms import Create_Activity
from .models import Activity

from django.db import connection #para ejecutar RAW queries

#Practica DRF
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, ActivitySerializer

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.core.serializers import serialize

import json
# locations = cod_des-cod_or	cod_des-cod_or1,cod_or2,cod_or3


#Practica DRF
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@csrf_exempt
def activity_list(request):
    """
    Devuelve las actividades registradas en formato GeoJson
    """
    if request.method == 'GET':
    	return HttpResponse(serialize('geojson', Activity.objects.all(), geometry_field='geom', fields=('id', 'date', 'place', 'name', 'description', 'num_person', 'instruments', 'focus', 'vos', 'result')))

# @csrf_exempt
# def activity_for_date(request, date_s, date_f):
#     """
#     Devuelve las actividades registradas por rango de fechas en formato GeoJson
#     """
#     return HttpResponse(serialize('geojson', Activity.objects.filter(date__range=(date_s, date_f)), geometry_field='geom', fields=('id', 'date', 'place', 'name', 'description', 'num_person', 'instruments', 'focus', 'vos', 'result')))

@csrf_exempt
def activity_for_date(request, date_s, date_f):
	"""
	Devuelve las actividades registradas por rango de fechas en formato GeoJson
	"""
	with connection.cursor() as cursor:
		cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (SELECT id, date, place, name, description, num_person, geom, instruments, focus, vos, result FROM backend_activity WHERE date BETWEEN %s AND %s ORDER BY id) as lp) As f) As fc;", [date_s, date_f])
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))

@csrf_exempt
def presence_for_year(request, date_s, date_f):
	"""
	Devuelve los municipios donde habia llegado la legion por rango de años
	"""
	with connection.cursor() as cursor:
		#cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select m.id, m.nombre_mpi, min(a.date), ST_Transform(ST_ForceRHR(m.geom), 4326) as geom from municipios m, backend_activity a where a.date BETWEEN %s AND %s AND ST_Within(ST_Transform(a.geom, 4326), ST_Transform(m.geom, 4326))=true group by m.id order by nombre_mpi) as lp) As f) As fc;", [date_s, date_f])
		cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select m.id, min(m.nombre_mpi) as mpi, ST_RotateX(ST_Translate(T_Transform(min(m.geom),4326), 0.03, 0.05), 0.1) as geom from (select geom, date from backend_activity where date BETWEEN %s AND %s) as a join (select id, geom, nombre_mpi from municipios) as m ON ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true group by m.id) as lp) As f) As fc;", [date_s, date_f])
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))

@csrf_exempt
def activity_for_municipio(request, date_s, date_f, pk_mun):
	"""
	Devuelves las actividades realizadas en un municpio en un rango de fechas en formato GeoJson
	"""
	with connection.cursor() as cursor:
		cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lg.geom)::json As geometry, row_to_json(lp) As properties FROM backend_activity As lg INNER JOIN (SELECT id, date, place, name, description, num_person, instruments, focus, vos, result FROM backend_activity) As lp ON lg.id = lp.id, municipios m WHERE m.id=%s AND lp.date BETWEEN %s AND %s AND ST_Within(lg.geom,  ST_RotateX(ST_Translate(ST_Transform(m.geom, 4326), 0.03, 0.05), 0.1))=true) As f) As fc;", [pk_mun, date_s, date_f])
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))
	# return HttpResponse(serialize('geojson', Activity.objects.filter(geom__within=poly, date__range=(date_s, date_f)), geometry_field='geom', fields=('name',)))

@csrf_exempt
def municipios(request):
	"""
	Devuelve todos los municipios en formato GeoJson
	"""
	with connection.cursor() as cursor:
		cursor.execute("SELECT row_to_json(fc) FROM (SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select id, nombre_mpi, ST_RotateX(ST_Translate(ST_Transform(ST_ForceRHR(geom), 4326), 0.03, 0.05), 0.1) as geom from municipios) as lp) As f) As fc;")
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))

@csrf_exempt
def municipios_mod(request):
	"""
	Devuelve todos los municipios modificando su ubicacion en formato GeoJson
	"""
	with connection.cursor() as cursor:
		cursor.execute("SELECT row_to_json(fc) FROM (SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select id, nombre_mpi, ST_RotateX(ST_Translate(ST_Transform(ST_ForceRHR(geom), 4326), 0.01, 0.05), 0.1) as geom from municipios) as lp) As f) As fc;")
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))

@csrf_exempt
def nodes(request):
	"""
	Devuelve el centroide de cada uno de los municipios donde la legión del afecto realizó actividades, detallando cuantas actividades se realizaron por cada municipio
	"""
	with connection.cursor() as cursor:
		#cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select m.nombre_mpi, ST_RotateX(ST_Translate(ST_Transform(min(ST_Centroid(m.geom)), 4326), 0.03, 0.05), 0.1) as geom, count(m.nombre_mpi) as num from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true group by m.nombre_mpi order by m.nombre_mpi ASC) as lp) As f) As fc;")
		cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select m.nombre_mpi, ST_Centroid(ST_RotateX(ST_Translate(ST_Transform(min(m.geom), 4326), 0.03, 0.05), 0.1)) as geom, count(m.nombre_mpi) as num from municipios m, backend_activity a where ST_Contains(ST_RotateX(ST_Translate(ST_Transform(m.geom, 4326), 0.03, 0.05), 0.1), a.geom)=true group by m.nombre_mpi order by m.nombre_mpi ASC) as lp) As f) As fc;")
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))

@csrf_exempt
def nodes_cant_person(request):
	"""
	Devuelve el centroide de cada uno de los municipios donde la legión del afecto realizó actividades, detallando cuantas personas fueron impactadas en cada municipio
	"""
	with connection.cursor() as cursor:
		#cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select m.id, m.nombre_mpi, sum(a.num_person) as cant_person,  ST_RotateX(ST_Translate(ST_Transform(ST_Centroid(m.geom), 4326), 0.01, 0.05), 0.1) as geom from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true group by m.id order by m.nombre_mpi ASC) as lp) As f) As fc;")
		cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select m.id, m.nombre_mpi, sum(a.num_person) as cant_person, ST_Centroid(ST_RotateX(ST_Translate(ST_Transform(min(m.geom), 4326), 0.03, 0.05), 0.1)) as geom from municipios m, backend_activity a where ST_Contains(ST_RotateX(ST_Translate(ST_Transform(m.geom, 4326), 0.03, 0.05), 0.1), a.geom)=true group by m.id order by m.nombre_mpi ASC) as lp) As f) As fc;")
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))


@csrf_exempt
def network(request):
	"""
	Devuelve la red de nodos del proyecto Legión del Afecto
	"""
	with connection.cursor() as cursor:
		cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lp.geom)::json As geometry, row_to_json(lp) As properties FROM (select r.mpi1, r.mpi2, ST_MakeLine(r.geom1, r.geom2) as geom, r.distance from (select DISTINCT ON (n1.nombre_mpi) n1.id as id1, n1.nombre_mpi as mpi1, n1.geom as geom1, n1.date as date1, n2.id as id2, n2.nombre_mpi as mpi2, n2.geom as geom2, n2.date as date2, ST_Distance(n1.geom, n2.geom) as distance from (select DISTINCT ON (m.nombre_mpi) m.id, m.nombre_mpi, ST_Transform(ST_Centroid(m.geom), 4326) as geom, a.date from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true order by m.nombre_mpi ASC, a.date ASC) n1, (select DISTINCT ON (m.nombre_mpi) m.id, m.nombre_mpi, ST_Transform(ST_Centroid(m.geom), 4326) as geom, a.date from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true order by m.nombre_mpi ASC, a.date ASC) n2 where n1.id <> n2.id order by n1.nombre_mpi asc, distance asc) as r order by r.mpi1) as lp) As f) As fc;")
		row = cursor.fetchone()
	return HttpResponse(json.dumps(row[0]))

@csrf_exempt
def network2(request):
	"""
	Devuelve la red de nodos del proyecto Legión del Afecto, cada nodo debe estar unido a los 2 nodos mas cercanos
	"""
	i = 0
	j = 0
	k = 0
	fc = {'type':'FeatureCollection','features':[]}
	adds = dict()

	
	with connection.cursor() as cursor:
		cursor.execute("select r.mpi1, r.mpi2, ST_MakeLine(r.geom1, r.geom2) as geom, r.distance from (select n1.id as id1, n1.nombre_mpi as mpi1, n1.geom as geom1, n1.date as date1, n2.id as id2, n2.nombre_mpi as mpi2, n2.geom as geom2, n2.date as date2, ST_Distance(n1.geom, n2.geom) as distance from (select DISTINCT ON (m.nombre_mpi) m.id, m.nombre_mpi, ST_Transform(ST_Centroid(m.geom), 4326) as geom, a.date from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true order by m.nombre_mpi ASC, a.date ASC) n1, (select DISTINCT ON (m.nombre_mpi) m.id, m.nombre_mpi, ST_Transform(ST_Centroid(m.geom), 4326) as geom, a.date from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true order by m.nombre_mpi ASC, a.date ASC) n2 where n1.id <> n2.id order by n1.nombre_mpi asc, distance asc) as r order by r.mpi1;")
		rows = cursor.fetchall()
		for j in range(len(rows)):
			key = rows[j][0]
			key = key.replace(" ", "")
			key = key.replace("ñ", "n")
			print(key, rows[j][3])
			if not key in adds.keys():
				adds[key] = 0
			if adds[key] < 1:
				line = GEOSGeometry(rows[j][2])
				#l1.append(list(line.coords[0]))
				#l1.append(list(line.coords[1]))
				f2 = {'type':'Feature','geometry':{'type':'LineString','coordinates':[]},'properties':{}}
				f2['geometry']['coordinates'] = line.coords
				adds[key] = adds[key] + 1
				fc['features'].append(f2)
			i = i +1
		#print(adds)
	return HttpResponse(json.dumps(fc))
	#return HttpResponse(l1)

@csrf_exempt
def local_networks(request):
	"""
	Devuelve la redes locales de la legion del afecto. Cada red local debe estar unida con otro red local
	"""
	i = 0
	j = 0
	k = 0
	fc = {'type':'FeatureCollection','features':[]}
	adds = dict()
	nodes = dict()#diccionario con todos los nodos, con su respectiva clave
	main_nodes = [378, 428, 212, 640, 1108, 756, 872, 879, 725, 773, 387, 917, 984, 816, 723, 514, 259, 180, 22, 77, 104, 37]
	second_nodes = [[369,368,411], [465,474,435,390,523,505,408,406,375,395,401,449], [178,219,202], [615], 
	[557,1107,605,607,544], [697, 613], [848, 890, 869, 832, 877], [827, 885, 893, 868], [685, 587, 710, 714, 693, 591, 563], 
	[748, 755, 752, 778], [293, 298, 184, 163, 1119, 277, 235], [1031, 970, 991, 961, 931, 953, 1027, 1045, 994, 997], 
	[921], [799, 801, 901, 884, 642], [762, 784, 758, 639], [535, 493, 527, 534, 515, 503, 520, 568, 540, 565, 402], 
	[198, 196, 233, 199, 200, 252, 258], [131, 241, 181], [6, 87, 109, 136, 149], [100, 139, 78, 85, 112, 142, 99, 1093, 137, 155, 145, 159], 
	[86, 90, 1104, 91, 72, 123], [80, 81, 74, 73]]
	
	# local1 = [369,368,411]
	# local2 = [465,474,435,390,523,505,408,406,375,395,401,449]
	# local3 = [438,452,522]#pendiente por nodo central marmato
	# local4 = [178,219,202]
	# local5 = [615]
	# local6 = [557,1107,605,607,544]
	# local7 = [697, 613]
	# local8 = [848, 890, 869, 832, 877]
	# local9 = [827, 885, 893, 868]
	# local10 = [685, 587, 710, 714, 693, 591, 563]
	# local11 = [748, 755, 752, 778]
	# local12 = [293, 298, 184, 163, 1119, 277, 235]
	# local13 = [, 1028] #falta pasto
	# local14 = [1031, 970, 991, 961, 931, 953, 1027, 1045, 994, 997]
	# local15 = [921]
	# local16 = [799, 801, 901, 884, 642]
	# local17 = [762, 784, 758, 639]
	# local18 = [535, 493, 527, 534, 515, 503, 520, 568, 540, 565, 402]
	# local19 = [198, 196, 233, 199, 200, 252, 258]
	# local20 = [131, 241, 181]
	# local21 = [6, 87, 109, 136, 149]
	# local22 = [100, 139, 78, 85, 112, 142, 99, 1093, 137, 155, 145, 159]
	# local23 = [86, 90, 1104, 91, 72, 123]
	# local24 = [80, 81, 74, 73]


	with connection.cursor() as cursor:
		#cursor.execute("select min(m.id) as id, m.nombre_mpi as nombre, min(ST_RotateX(ST_Translate(ST_Transform(ST_Centroid(m.geom), 4326), 0.01, 0.05), 0.1)) as geom from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true group by m.nombre_mpi order by id;")
		cursor.execute("select min(m.id) as id, m.nombre_mpi as nombre, ST_Centroid(ST_RotateX(ST_Translate(ST_Transform(min(m.geom), 4326), 0.03, 0.05), 0.1)) as geom from municipios m, backend_activity a where ST_Contains(ST_Transform(m.geom, 4326), a.geom)=true group by m.nombre_mpi order by id;")
		rows = cursor.fetchall()
		for row in rows:
			if(not row[0] in nodes.keys()):
				nodes[row[0]] = {"id":row[0], "nombre":row[1], "geom":row[2]}
	
	for i in range(len(main_nodes)):
		p1 = GEOSGeometry(nodes[main_nodes[i]]["geom"])
		for j in range(len(second_nodes[i])):
			p2 = GEOSGeometry(nodes[second_nodes[i][j]]["geom"])
			line1 = LineString(p1.coords, p2.coords)
			with connection.cursor() as cursor:
				cursor.execute("select ST_CurveToLine('CIRCULARSTRING(' || st_x(st_startpoint(%s)) || ' ' || st_y(st_startpoint(%s)) || ', ' || st_x(st_centroid(ST_OffsetCurve(%s, st_length(%s)/10, 'quad_segs=4 join=bevel'))) || ' ' || st_y(st_centroid(ST_OffsetCurve(%s, st_length(%s)/10, 'quad_segs=4 join=bevel'))) || ', ' || st_x(st_endpoint(%s)) || ' ' ||  st_y(st_endpoint(%s)) || ')') AS the_curved_geom;", [line1.wkt,line1.wkt,line1.wkt,line1.wkt,line1.wkt,line1.wkt,line1.wkt,line1.wkt])
				row2 =  cursor.fetchone()
				line1 = GEOSGeometry(row2[0])
			f1 = {'type':'Feature','geometry':{'type':'LineString','coordinates':[]},'properties':{'nombre':''}}
			f1['properties']['nombre'] = nodes[main_nodes[i]]["nombre"] + "-" + nodes[second_nodes[i][j]]["nombre"]
			f1['geometry']['coordinates'] = line1.coords
			fc['features'].append(f1)
			# for k in range(j, len(second_nodes[i])-1):
			# 	p3 = GEOSGeometry(nodes[second_nodes[i][k+1]]["geom"])
			# 	line2 = LineString(p2.coords, p3.coords)
			# 	with connection.cursor() as cursor:
			# 		cursor.execute("select ST_CurveToLine('CIRCULARSTRING(' || st_x(st_startpoint(%s)) || ' ' || st_y(st_startpoint(%s)) || ', ' || st_x(st_centroid(ST_OffsetCurve(%s, st_length(%s)/10, 'quad_segs=4 join=bevel'))) || ' ' || st_y(st_centroid(ST_OffsetCurve(%s, st_length(%s)/10, 'quad_segs=4 join=bevel'))) || ', ' || st_x(st_endpoint(%s)) || ' ' ||  st_y(st_endpoint(%s)) || ')') AS the_curved_geom;", [line2.wkt,line2.wkt,line2.wkt,line2.wkt,line2.wkt,line2.wkt,line2.wkt,line2.wkt])
			# 		row3 =  cursor.fetchone()
			# 		line2 = GEOSGeometry(row3[0])
			# 	f2 = {'type':'Feature','geometry':{'type':'LineString','coordinates':[]},'properties':{'nombre':''}}
			# 	f2['properties']['nombre'] = nodes[second_nodes[i][j]]["nombre"] + "-" + nodes[second_nodes[i][j+1]]["nombre"]
			# 	f2['geometry']['coordinates'] = line2.coords
			# 	fc['features'].append(f2)

		if k==0:
			print(line1.coords)
			#print(p1.coords)
			#print(p2.coords)

		k = k + 1

	return HttpResponse(json.dumps(fc))
	# 	for j in range(len(rows)):
	# 		key = rows[j][0]
	# 		key = key.replace(" ", "")
	# 		key = key.replace("ñ", "n")
	# 		print(key, rows[j][3])
	# 		if not key in adds.keys():
	# 			adds[key] = 0
	# 		if adds[key] < 1:
	# 			line = GEOSGeometry(rows[j][2])
	# 			#l1.append(list(line.coords[0]))
	# 			#l1.append(list(line.coords[1]))
	# 			f2 = {'type':'Feature','geometry':{'type':'LineString','coordinates':[]},'properties':{}}
	# 			f2['geometry']['coordinates'] = line.coords
	# 			adds[key] = adds[key] + 1
	# 			fc['features'].append(f2)
	# 		i = i +1
	# 	print(adds)
	# return HttpResponse(json.dumps(fc))
	return HttpResponse("Ejecutado Exitosamente")

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

def get_geometries(request):
	activities = Activity.objects.all()
	file = open('geometries.txt','w')
	for act in activities:
		pnt = GEOSGeometry(act.geom)
		print(pnt.coords[0])
		file.write(str(pnt.coords[0])+";"+str(pnt.coords[1])+"\n")	
	return HttpResponse("Se ha generado el archivo con las geometrias exitosamente")

def create_activity(request):
	if request.method == 'POST':
		form = Create_Activity(request.POST)
		if form.is_valid():
			date = form.cleaned_data['date']
			place = form.cleaned_data['place']
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']
			num_person = form.cleaned_data['num_person']
			geom_WKT = form.cleaned_data['geom']
			instruments = form.cleaned_data['instruments']
			focus = form.cleaned_data['focus']
			vos = form.cleaned_data['vos']
			result = form.cleaned_data['result']
			geom = GEOSGeometry(geom_WKT)
			act = Activity(date = date, place = place, name = name, description = description, num_person = num_person, geom = geom,
					instruments = instruments, focus = focus, vos = vos, result = result)
			act.save()
			form = Create_Activity()
			return render(request, 'backend/form.html', {'form': form})
		else:
			return render(request, 'backend/form.html', {'form': form})
	else:
		form = Create_Activity()
	return render(request, 'backend/form.html', {'form': form})

def edit_activity(request, pk, geom_WKT):
	# return HttpResponse("pk: " + str(pk) + " geom_WKT: " + geom_WKT)
	act = Activity.objects.get(id=pk)
	geom = GEOSGeometry(geom_WKT)
	act.geom = geom
	act.save()
	return HttpResponse("Edit Ok")

def upload2007(request):
	# return HttpResponse("Se cargaran las actividades del 2007")
	i = 2
	with open('DB_2007_mod.tsv','r') as tsv:
		for line in tsv:
			field = line.strip().split('\t')
			date = conv_date(field[0])
			place = field[1]
			name = field[2]
			description = field[3]
			num_person = field[4]
			geom_WKT = field[5]
			instruments = ""
			focus = ""
			vos = ""
			result = ""
			try:
				geom = GEOSGeometry(geom_WKT)
			except ValueError:
				print("Se produjo un error con la geometria: ", i, geom_WKT)
			print(i, date, place, name, description, num_person, geom.geom_type)
			act = Activity(date = date, place = place, name = name, description = description, num_person = num_person, geom = geom,
					instruments = instruments, focus = focus, vos = vos, result = result)
			act.save()
			i += 1
	return HttpResponse("Load Ok")

def upload2013(request):
	i = 2
	with open('DB_2013_mod.tsv','r') as tsv:
		for line in tsv:
			field = line.strip().split('\t')
			date = conv_date(field[3])
			place = field[2]
			name = field[1]
			description = field[0]
			num_person = field[4].replace(".", "")
			lon = fix_lon(field[6])
			lat = fix_lat(field[7])
			geom_WKT = "POINT(" + lon + " " + lat + ")"			
			instruments = field[5]
			focus = ""
			vos = ""
			result = ""
			geom = GEOSGeometry(geom_WKT)
			act = Activity(date = date, place = place, name = name, description = description, num_person = num_person, geom = geom,
					instruments = instruments, focus = focus, vos = vos, result = result)
			act.save()
			print(i, date, place, name, description, num_person, geom.geom_type)
			i += 1
	return HttpResponse("Load 2013 Ok")
	# return HttpResponse("Se cargaran las actividades del 2013")

def upload2009(request):
	i = 2
	with open('DB_2009_mod.tsv','r') as tsv:
		for line in tsv:
			field = line.strip().split('\t')
			date = conv_date(field[0])
			place = field[1]
			name = ""
			description = field[2]
			num_person = int(field[3].replace(".", ""))
			geom_WKT = field[4]
			instruments = ""
			focus = ""
			vos = ""
			result = ""
			geom = GEOSGeometry(geom_WKT)
			act = Activity(date = date, place = place, name = name, description = description, num_person = num_person, geom = geom,
					instruments = instruments, focus = focus, vos = vos, result = result)
			act.save()
			print(i, date, place, name, description, num_person, geom.geom_type)
			i += 1
	return HttpResponse("Load 2009 Ok")
	# return HttpResponse("Se cargaran las actividades del 2009")

def upload2014(request):
	i = 1
	with open('DB_2014_mod.tsv','r') as tsv:
		for line in tsv:
			field = line.strip().split('\t')
			date = conv_date_new(field[1])
			place = field[0]
			name = field[6]
			description = field[4]
			num_person = int(field[2].replace(".", ""))
			lon = fix_lon(field[7])
			lat = fix_lat(field[8])
			geom_WKT = "POINT(" + lon + " " + lat + ")"
			instruments = ""
			focus = field[3]
			vos = field[5]
			result = ""
			geom = GEOSGeometry(geom_WKT)
			act = Activity(date = date, place = place, name = name, description = description, num_person = num_person, geom = geom,
					instruments = instruments, focus = focus, vos = vos, result = result)
			act.save()
			print(i, date, place, name, description, focus, vos, num_person, geom.geom_type)
			i += 1
	return HttpResponse("Load 2014 Ok")

def upload2015(request):
	i = 2
	with open('DB_2015_mod.tsv','r') as tsv:
		for line in tsv:
			field = line.strip().split('\t')
			date = conv_date(field[1])
			place = field[2]
			name = field[0]
			description = field[4]
			num_person = int(field[3].replace(".", ""))
			lon = fix_lon(field[6])
			lat = fix_lat(field[5])
			geom_WKT = "POINT(" + lon + " " + lat + ")"
			instruments = ""
			focus = ""
			vos = ""
			result = ""
			geom = GEOSGeometry(geom_WKT)
			act = Activity(date = date, place = place, name = name, description = description, num_person = num_person, geom = geom,
					instruments = instruments, focus = focus, vos = vos, result = result)
			act.save()
			print(i, date, place, name, description, num_person, geom.geom_type)
			i += 1
	return HttpResponse("Load 2015 Ok")

#Convierte una fecha del tipo MM/DD/YYYY yo YYYY-MM-DD
def conv_date(d):
	l = d.split("/")
	return l[2] + "-" + l[0] + "-" + l[1]

#Convierte una fecha del tipo DD/MM/YYYY yo YYYY-MM-DD
def conv_date_new(d):
	l = d.split("-")
	return l[2] + "-" + l[1] + "-" + l[0]

#Arregla la longitud
def fix_lon(lon):
	lon = lon.strip()
	lon = lon.replace(".", "")
	lon = lon.replace(",", "")
	cadena = ""
	i = 0
	for l in lon:
		if i == 3:
			cadena += "."
		cadena += l
		i += 1
	return cadena

#Arregla la latitud
def fix_lat(lat):
	lat = lat.strip()
	lat = lat.replace(".", "")
	lat = lat.replace(",", "")
	cadena = ""
	i = 0
	for l in lat:
		if i == 1:
			cadena += "."
		cadena += l
		i += 1
	return cadena