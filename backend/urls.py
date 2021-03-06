from django.urls import include, path

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
    path('activities/', views.activity_list, name='activities'),
    path('activities/<str:date_s>/<str:date_f>', views.activity_for_date, name='activities-for-date'),
    path('activities/<str:date_s>/<str:date_f>/<str:pk_mun>', views.activity_for_municipio, name='activities-for-municipio'),
    path('nodes', views.nodes, name='nodes'),
    path('nodes/<str:date_s>/<str:date_f>', views.nodes_for_date, name='nodes-for-date'),
    path('total-activity-for-municipio', views.total_activity_for_municipio, name='total-activity-for-municipio'),
    path('nodes-cant-person', views.nodes_cant_person, name='nodes-cant-person'),
    path('network', views.network, name='network'),
    path('network2', views.network2, name='network2'),
    path('local-networks', views.local_networks, name='local-networks'),
    path('nacional-networks', views.nacional_networks, name='nacional-networks'),
    path('municipios', views.municipios, name='municipios'),
    path('presence-for-year/<str:date_s>/<str:date_f>', views.presence_for_year, name='presence-for-year'),
    # path('upload-shapes', views.upload_shapes, name='upload-shapes'),
    # path('users/', views.UserViewSet, name='users'),
    # path('groups/', views.GroupViewSet, name='groups'),
]
