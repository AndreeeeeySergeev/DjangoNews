from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Author_rating = models.IntegerField(default=5)

	def update_rating(self):
		post_rating = self.post_set.aggregate(postRating=Sum('rating'))
		pRat = 0
		pRat += post_rating.get('postRating')


		commentRat = self.user.comment_set.aggregate(commentRating=Sum('rating'))
		cRat = 0
		cRat += commentRat.get('commentRating')

		self.Author_rating = pRat * 3 + cRat
		self.save()

class Category(models.Model):
	category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	News = 'NW'
	STATEMENT = 'ST'
	CATEGORY_TYPE = (
		(News, 'Новость'),
		(STATEMENT, 'Статья')
	)
	Category_choices = models.CharField(max_length=2, choices=CATEGORY_TYPE, default=News)
	date = models.DateTimeField(auto_now_add=True)
	postCategory = models.ManyToManyField(Category, through='PostCategory')
	title = models.CharField(max_length=200)
	text = models.TextField()
	rating = models.IntegerField(default=0)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		if self.rating <= 0:
			return self.rating == 0
		else:
			self.rating -= 1
		self.save()


	def preview(self):
		return self.text[0:124] + "..."


class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
	comment = models.ForeignKey(Post, on_delete=models.CASCADE)
	commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
	commentText = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		if self.rating < 0:
			return self.rating == 0
		else:
			self.rating -= 1
		self.save()

# Create your models here.
