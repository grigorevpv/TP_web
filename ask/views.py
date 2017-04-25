from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms.forms import LoginForm
from ask.models import Question, QuestionManager, Answer, Tag, Logic
from django.contrib import auth
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
	tags = Tag.objects.all()[:5]
	user = auth.get_user(request)
	if user.is_authenticated:
		print("name = %s" % user.get_username())
		context = RequestContext(request, {
			'questions': page,
			't': tags,
			'user': user
		})
	else:
		print("not")
		context = RequestContext(request, {
			'questions': page,
			't': tags,
		})
	return HttpResponse(template.render(context))


def tag(request, tag_name):
	template = loader.get_template('ask/tag_content.html')
	questions = Logic.get_tag(tag_name)
	tags = Tag.objects.all()[:5]
	if questions:
		page = paginate(request, questions)
		context = RequestContext(request, {
			'tag_name': tag_name,
			'questions': page,
			't': tags
		})
		return HttpResponse(template.render(context))
	else:
		raise Http404


def question(request, question_id):
	template = loader.get_template('ask/question_content.html')
	question_ = Logic.get_question(question_id)
	answer_ = Logic.get_answers(question_id)
	# answer_ = Question.objects.all()
	tags = Tag.objects.all()[:5]
	page = paginate(request, answer_)
	context = RequestContext(request, {
		'question': question_,
		'answer': page,
		't': tags
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

	return render(request, 'ask/login_content.html', {'form': form})


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('hot/')


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





