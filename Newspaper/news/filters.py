from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, DateTimeFilter
from .models import Post, Category

class PostFilter(FilterSet):
	# 	material = ModelChoiceFilter(
	# 	field_name='productmatrial__material',
	# 	queryset=Material.objects.all(),
	# 	label='Material',
	# 	# empty_label='Любой',
	# 	conjoined=True,
	# )

	category = ModelChoiceFilter(
		field_name='postcategory__categoryThrough',
		queryset=Category.objects.all(),
		label='Category',
		empty_label='Любой'
	)

	added_after = DateTimeFilter(
		field_name='dateCreation',
		lookup_expr='gt',
		label='Date Creation',
		widget=DateTimeInput(
			format='%Y-%m-%dT%H:%M',
			attrs={'type': 'datetime-local'},
		)
	)

	class Meta:
		model = Post
		fields = {
			'title': ['iexact'],
			'categoryType': ['exact'],
		}