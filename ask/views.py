from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

QUESTIONS = {
    '1': {'id': 1, 'title': 'I`m your dream', 'text': 'I`m your dream, make you real'},
    '2': {'id': 2, 'title': 'I`m your eyes', 'text': 'I`m your eyes when you must steal'},
    '3': {'id': 3, 'title': 'I`m your pain', 'text': 'I`m your pain when you can`t feel'},
}


def questions_list(request):
    return render(request, 'ask/main_content.html', {'questions': QUESTIONS.values()})

def ask(request):
	template = loader.get_template('ask/ask_content.html')
	context = RequestContext(request, {
		})
	return HttpResponse(template.render(context))

def hot(request):
	template = loader.get_template('ask/main_content.html')
	questions = {}
	tags = ['Moon', 'Park']
	for i in xrange(1,55):
		questions[i] = {
			'title': 'title' + str(i),
			'id': i,
			'text': 'text' + str(i),
			'tags': tags,
			}
	
	questions = tuple(questions.items())
	paginator = Paginator(questions, 4)
	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		questions = paginator.page(paginator.num_pages)

	context = RequestContext(request, {
		'questions': questions,
		})
	return HttpResponse(template.render(context))

def tag(request, tagName):
	template = loader.get_template('ask/tag_content.html')
	questions = {}
	tags = [tagName]
	for i in xrange(1,43):
		questions[i] = {
			'title': 'title' + str(i),
			'id': i,
			'text': 'text' + str(i),
			'tags': tags,
			}

	questions = tuple(questions.items())
	paginator = Paginator(questions, 4)
	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		questions = paginator.page(paginator.num_pages)

	context = RequestContext(request, {
		'tagName':tagName,
		'questions': questions,
		})
	return HttpResponse(template.render(context))

def question(request, question):
	template = loader.get_template('ask/question_content.html')
	questions = {}
	tags = ['Moon', 'Park']
	for i in xrange(1,4):
		questions[i] = {
			'title': 'title' + str(i),
			'id': i,
			'text': 'text' + str(i),
			'tags': tags,
			}
	question = {'title': 'title', 'id': 1, 'text': 'text', 'tags': tags,}
	context = RequestContext(request, {
		'question':question,
		'questions': questions.values(),
		})
	return HttpResponse(template.render(context))

def login(request):
	template = loader.get_template('ask/login_content.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

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

