from django.contrib import admin
from .models import Author, Post, Comment, Category

def nullfy_quantity(modeladmin, request, queryset):
	queryset.update(quantity=0)
nullfy_quantity.short_description = 'Обнулить новости'

class PostAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Post._meta.get_fields()]
	# list_display = ('author', 'title', 'on_rating')
	list_filter = ('author', 'title', 'on_rating')
	search_fields = ('author', 'category__name')
	actions = [nullfy_quantity]

class CategoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Category.__meta.get_fields()]
	list_filter = ('name', 'subscribers')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('text', 'dateCreation')
	list_filter = ('text', 'dateCreation')

class AuthorAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Author.__meta.get_fields()]
	list_filter = ('authorUser')

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.unregister(Category)
# Register your models here.
