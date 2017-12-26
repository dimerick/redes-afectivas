from django.http import HttpResponse

def index(request):
	with open('legion2003.tsv','r') as tsv:
		read = ""
		for line in tsv:
			field = line.strip().split('\t')
			read += str(field)
	return HttpResponse(read)