from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Activity


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ActivitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Activity
		fields = ('date', 'name', 'description', 'num_person', 'geom')