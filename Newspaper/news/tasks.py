from celery import shared_task, app
from django.core.mail import EmailMultiAlternatives
from Newspaper.settings import *
from django.dispatch import receiver
from .models import Post
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
import time


def send_notifications():
	html_context = render_to_string(
		'post_created_email.html',
		{'text': preview,
		 'link': f'https://127.0.0.1:8000/news/{pk}'}
	)

	msg = EmailMultiAlternatives(
		 subject='title',
		 body='',
		 from_email=setting.DEFAULT_FROM_EMAIL,
		 to=subscribers
	  )
	msg.attach_alternative(html_context, 'text/html')
	msg.send()

@shared_task
@receiver(m2m_changed, sender=Post)
def post_created(instance, sender, **kwargs):
	if kwargs['action'] == 'post_add':
		categories = instance.category.all()
		subscribers: list[str] = []
		for category in categories:
			subscribers += category.subscribers.all()

		subscribers = [s.email for s in subscribers]

		send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

@shared_task
def news_sender():
	today = datetime.datetime.now()
	last_week = today - datetime.timedelta(days=7)
	post = Post.objects.filter(dateCreation__gte=last_week)
	categories = set(post.values_list('postCategory__name', flat=True))
	subscribers = set(Category.objects.filter(name__in=categories).values_list
					  ('subscribers__email', flat=True))

	subject = 'Свежие новости!',

	html = render_to_string(
		'daily_post.html',
		{
			'link': f'https://127.0.0.1:8000',
			'post': post,
			}
		)
	msg = EmailMultiAlternatives(
		subject=subject, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers, )
	msg.attach_alternative(html, "text/html")
	msg.send()

# @shared_task
# def new_news():
# 	from news.signal import *
#
# @shared_task
# def news_of_week():
# 	from news.management.commands.runapscheduler import my_job