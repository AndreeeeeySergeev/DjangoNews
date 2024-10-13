from .models import *
from rest_framework import serializers

class PostSerializers(serializers.HyprtlinkedModelSerializers):
	class Meta:
		model = Post
		fields = ['id', 'title']

class CategorySerializers(serializers.HyprtlinkedModelSerializers):
	class Meta:
		model = Category
		fields = ['name']