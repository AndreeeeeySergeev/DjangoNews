from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


@receiver(m2m_changed, sender=Post)
def post_created(instance, created, **kwargs):
	if not created:
		return

	emails = User.objects.filter(subscriptions__category=instance.categoryType).values_list('email', flat=True)
	subject = f'Новая новость в категории {instance.category}'
	text_context = (
		f'Новость: {instance.title}\n'
		f'Рейтинг: {instance.rating}\n\n'
		f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
	)
	html_content = (
		f'Новость: {instance.title}<br>'
		f'Рейтинг: {instance.rating}<br><br>'
		f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
		f'Сcылка на новость </a>'
	)
	for email in emails:
		msg = EmailMultiAlternatives(subject, text_context, None, [email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
