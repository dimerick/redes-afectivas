from django.contrib import admin

from .models import Activity

# class PntTraxGeoAdmin(admin.mapquestGeoAdmin):
#     """Base Class for Geometry Table Admin"""
#     list_display = ('name','collectDate','group','featurePurpose','collectionMethod')
#     list_editable = ('featurePurpose','group','collectionMethod')
#     list_filter = ('featurePurpose','group__name')
    
admin.site.register(Activity)
