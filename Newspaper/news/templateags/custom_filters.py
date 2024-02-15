import sys
sys.path.append("c:\Projects\DjangoNews\Newspaper\news")
import models
from models import Post
from django import template

register = template.Library()

@register.filter()
def censor(i):
	"""
	"""
	for i in Post.text.titlecase:
		Post.text.titlecase = "***"
