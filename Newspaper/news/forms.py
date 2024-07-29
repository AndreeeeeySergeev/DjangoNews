from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category

# class PostForm(forms.ModelForm):
# 	name = forms.CharField(label='Name')
# 	description = forms.CharField(label='Description')
# 	category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all())


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		# fields ='__all__'
		fields = [
			'title',
			'text',
			'author',
			'rating',
		]

	def clean(self):
		cleaned_data = super().clean()
		description = cleaned_data.get('text')
		if description is not None and len(description) < 20:
			raise ValidationError({'text': 'Описание не может быть менее 20 символов.'})
		name = cleaned_data.get('title')
		if name == description:
			raise ValidationError({'text': 'Описание не должно быть идентично названию.'})

		return cleaned_data


class ArtcileForm(forms.ModelForm):
	class Meta:
		model = Post
		# fields ='__all__'
		fields = [
			'title',
			'text',
			'author',
			'rating',
		]