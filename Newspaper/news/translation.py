from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions

@register(Post)
class PostTranslationOptions(TranslationOptions):
	fields = ('title', 'text', 'dateCreation', 'author',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
	fields = ('name', 'subscribers',)