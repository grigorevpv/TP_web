from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms.forms import LoginForm, AnswerForm, NewQuestionForm, RegisterForm
from ask.models import Question, QuestionManager, Answer, Tag, Logic, Profile
from django.contrib.auth import authenticate, login as LogIn, logout as LogOut, get_user
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
	context = {}
	form = NewQuestionForm
	context.update({'form': form})
	user = get_user(request)
	if not user.is_authenticated:
		user = None
	context.update({'user': user})
	response = render(request, 'ask/ask_content.html', context)
	return response


def hot(request):
	template = loader.get_template('ask/main_content.html')
	questions = Question.objects.best_questions()
	page = paginate(request, questions)
	tags = Tag.objects.all()[:5]
	user = get_user(request)
	if not user.is_authenticated:
		user = None
	context = RequestContext(request, {
		'questions': page,
		't': tags,
		'user': user
	})
	return HttpResponse(template.render(context))


def tag(request, tag_name):
	template = loader.get_template('ask/tag_content.html')
	user = get_user(request)
	if not user.is_authenticated:
		user = None
	questions = Logic.get_tag(tag_name)
	tags = Tag.objects.all()[:5]
	if questions:
		page = paginate(request, questions)
		context = RequestContext(request, {
			'tag_name': tag_name,
			'questions': page,
			't': tags,
			'user': user
		})
		return HttpResponse(template.render(context))
	else:
		raise Http404


def question(request, question_id):
	template = loader.get_template('ask/question_content.html')
	user = get_user(request)
	if not user.is_authenticated:
		user = None
	question_ = Logic.get_question(question_id)
	answer_ = Logic.get_answers(question_id)
	# answer_ = Question.objects.all()
	tags = Tag.objects.all()[:5]
	page = paginate(request, answer_)
	context = RequestContext(request, {
		'question': question_,
		'answer': page,
		't': tags,
		'user': user
	})
	return HttpResponse(template.render(context))


def login(request):
	redirect_to = request.GET.get('next', '/ask/hot/')
	context = {}
	if request.method == 'POST':
		form = LoginForm(request.POST)
		context.update({'user': get_authenticate_user(request)})
		if form.login_user(request):
			return HttpResponseRedirect(redirect_to)
	else:
		form = LoginForm()
	context.update({'form': form})
	response = render(request, 'ask/login_content.html', context)
	return response


def logout(request):
	LogOut(request)
	return HttpResponseRedirect('hot/')


def signup(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/ask/hot/')
	context = ({'user': get_authenticate_user(request)})
	form = RegisterForm()

	try:
		path = request.GET['continue']
		print('continue')
	except KeyError:
		path = '/ask/hot/'

	if request.method == 'POST':
		form = RegisterForm(request.POST, request.FILES)
		if form.save_user():
			return HttpResponseRedirect(path)
		else:
			HttpResponseRedirect('/ask/hot/#')

	user = get_authenticate_user(request)
	context.update({'user': user, 'form': form})
	return render(request, 'ask/signup_content.html', context)


def list(request, list):
	return HttpResponse("You're at the %s page" % list)


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


def get_authenticate_user(request):
	if request.user.is_authenticated():
		user = Profile.objects.get(user_id=request.user.id)
	else:
		user = None
	return user
