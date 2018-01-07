from django import forms

class Create_Activity(forms.Form):
	date = forms.DateField(label="Fecha *", error_messages={'invalid':'La fecha debe estar en el formato AAAA-MM-DD'})
	place = forms.CharField(label="Lugar *", strip=True, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))
	name = forms.CharField(label="Nombre *", strip=True, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))
	description = forms.CharField(label="Descripción *", strip=True, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))
	num_person = forms.IntegerField(label="No Asistentes *", min_value=0)
	geom = forms.CharField(label="Geometria en formato WKT *", strip=True, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))
	instruments = forms.CharField(label="Instrumentos", strip=True, required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))
	focus = forms.CharField(label="Focos", strip=True, required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))
	vos = forms.CharField(label="Ver, oir y sentir", strip=True, required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))
	result = forms.CharField(label="Resultados", strip=True, required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows':10}))



