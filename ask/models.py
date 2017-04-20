from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

GOOD_RATING = 5


class Profile(models.Model):
	avatar = models.ImageField(upload_to="avatars/")
	user = models.OneToOneField(User)


class QuestionManager(models.Manager):
	def best_questions(self):
		return self.filter(rating__gt=GOOD_RATING).order_by('-rating')

	def new_questions(self):
		return self.order_by('-created')


class Question(models.Model):
	title = models.CharField(max_length=60)
	text = models.TextField()
	auth = models.ForeignKey(User)
	rating = models.IntegerField(default=0)
	created = models.DateTimeField(default=datetime.now)
	tags = models.ManyToManyField('Tag')
	like = models.IntegerField(default=0)

	objects = QuestionManager()

	def nace_title(self):
		return self.title + '?'

	def __unicode__(self):
		return u'{0}-{1}'.format(self.id, self.title)


class Answer(models.Model):
	created = models.DateTimeField(default=datetime.now)
	question = models.ForeignKey(Question, null=True)
	text = models.CharField(max_length=200)
	auth = models.ForeignKey(User)
	rating = models.IntegerField(default=0)
	correct = models.BooleanField(default=False)
	like = models.IntegerField(default=0)

	def __unicode__(self):
		return u'{0}-{1}'.format(self.id, self.text[:60])


class Tag(models.Model):
	name = models.CharField(max_length=60)


class Logic:

	@staticmethod
	def get_tag(tag):
		test_tag = Tag.objects.filter(name=tag)
		if test_tag:
			return Question.objects.new_questions().filter(tags__name__exact=tag)
		else:
			Question.objects.none()

	@staticmethod
	def get_question(question_id):
		test_question = Question.objects.get(id__exact=question_id)
		if test_question:
			return test_question
		else:
			Question.objects.none()

	@staticmethod
	def get_answers(question_id):
		test_answers = Answer.objects.filter(id=question_id)
		if test_answers:
			return test_answers.order_by('-created')
		else:
			Question.objects.none()







