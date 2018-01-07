from django.urls import path

from . import views

app_name = 'redes-afectivas'
urlpatterns = [
    path('backend', views.index, name='index'),
    path('create-activity', views.create_activity, name='create-activity'),
]
