from django.urls import path

from . import views

app_name = 'redes-afectivas'
urlpatterns = [
    path('backend', views.index, name='index'),
    path('create-activity', views.create_activity, name='create-activity'),
    path('edit-activity/<int:pk>/<geom_WKT>', views.edit_activity, name='edit-activity'),
    path('upload-2007/', views.upload2007, name='upload-2007'),
    path('upload-2013/', views.upload2013, name='upload-2013'),
    path('upload-2009/', views.upload2009, name='upload-2009'),
    path('upload-2014/', views.upload2014, name='upload-2014'),
    path('upload-2015/', views.upload2015, name='upload-2015'),
    path('get-geometries/', views.get_geometries, name='get-geometries'),
]
