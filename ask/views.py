from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms.forms import LoginForm
from ask.models import Question, QuestionManager, Answer, Tag, Logic
from django.shortcuts import render_to_response


def paginate(request, qs):
	try:
		limit = int(request.GET.get('limit', 3))
	except ValueError:
		limit = 3
	if limit > 100:
		limit = 6
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		raise Http404
	paginator = Paginator(qs, limit)
	try:
		page = paginator.page(page)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return page


def ask(request):
	template = loader.get_template('ask/ask_content.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))


def hot(request):
	template = loader.get_template('ask/main_content.html')
	questions = Question.objects.best_questions()
	page = paginate(request, questions)
	context = RequestContext(request, {
		'questions': page,
	})
	return HttpResponse(template.render(context))


def tag(request, tag_name):
	template = loader.get_template('ask/tag_content.html')
	questions = Logic.get_tag(tag_name)
	if questions:
		page = paginate(request, questions)
		context = RequestContext(request, {
			'tag_name': tag_name,
			'questions': page,
		})
		return HttpResponse(template.render(context))
	else:
		raise Http404


def question(request, question_id):
	template = loader.get_template('ask/question_content.html')
	question_ = Logic.get_question(question_id)
	# answer_ = Logic.get_answers(question_id)
	answer_ = Question.objects.all()
	page = paginate(request, answer_)
	context = RequestContext(request, {
		'question': question_,
		'answer': page,
	})
	return HttpResponse(template.render(context))


def login(request):
	template = loader.get_template('ask/login_content.html')

	form = LoginForm()

	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			return HttpResponse('thanks')

		else:
			form = LoginForm()

	return render(request, 'ask/login_content.html', {'form': form} )

# context = RequestContext(request, {
# 	'form': form,
# 	})
# return HttpResponse(template.render(context))

def signup(request):
	template = loader.get_template('ask/signup_content.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def list(request, list):
	return HttpResponse("You're at the %s page" %list)

def hello(request):
	return HttpResponse("Hello, world. You're at the ask index.")

@csrf_exempt
def get_post(request):
	template = loader.get_template('ask/get_post.html')

	if request.method == 'GET':
		name = request.GET.get("name", "")
		age = request.GET.get("age", "")
		context = RequestContext(request, {
			'name': name,
			'age': age,
		})
	elif request.method == 'POST':
		group = request.POST.get("group", "")
		course = request.POST.get("course", "")
		context = RequestContext(request, {
			'group': group,
			'course': course,
		})

	return HttpResponse(template.render(context))

# ------------------------------------------------
# from __future__ import unicode_literals
#
# from django.db import models
# from django.contrib.auth.models import User
# from datetime import datetime
#
# GOOD_RATING = 10
#
#
# class Profile(models.Model):
# 	avatar = models.ImageField(upload_to="avatars/")
# 	user = models.OneToOneField(User)
#
#
# class QuestionManager(models.Manager):
# 	def best_questions(self):
# 		self.filter(rating__gt=GOOD_RATING).order_by('-rating')
#
# 	def new_questions(self):
# 		return self.order_by('-created_at')
#
# 	def get_tag(self, tag):
# 		testtag = Tag.objects.filter(name=tag)
# 		if testtag:
# 			return Question.objects.best_questions().filter(tag__name__exact=tag)
# 		else:
# 			Question.objects.none()
#
#
# class Question(models.Model):
# 	title = models.CharField(max_length=60)
# 	text = models.TextField()
# 	auth = models.ForeignKey(User)
# 	rating = models.IntegerField()
# 	created = models.DateTimeField(default=datetime.now)
# 	tags = models.ManyToManyField('Tag')
# 	like = models.IntegerField(default=0)
#
# 	objects = QuestionManager()
#
# 	def nace_title(self):
# 		return self.title + '?'
#
# 	def __unicode__(self):
# 		return u'{0}-{1}'.format(self.id, self.title)
#
#
# class Answer(models.Model):
# 	created = models.DateTimeField(default=datetime.now)
# 	question = models.ForeignKey(Question, null=True)
# 	text = models.CharField(max_length=200)
# 	auth = models.ForeignKey(User)
# 	rating = models.IntegerField(default=0)
# 	correct = models.BooleanField(default=False)
# 	like = models.IntegerField(default=0)
#
# 	def __unicode__(self):
# 		return u'{0}-{1}'.format(self.id, self.text[:60])
#
#
# class Tag(models.Model):
# 	name = models.CharField(max_length=60)
#
#
#



