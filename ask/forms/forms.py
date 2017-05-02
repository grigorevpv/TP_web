from django import forms
from django.contrib import auth
from ask.models import Profile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	login = forms.CharField(label='Login', max_length=100, help_text='Enter your login...')
	password = forms.CharField(label='Login', max_length=100, widget=forms.PasswordInput())

	def login_user(self, request):
		if self.is_valid():
			user = auth.authenticate(username=self.cleaned_data.get('login'),
									 password=self.cleaned_data.get('password'))
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					return True
				else:
					self.add_error(None, 'Your account is blocked')
			else:
				self.add_error(None, 'Error in login or password')
		return False


class RegisterForm(forms.Form):
	login = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=30)
	nickName = forms.CharField(max_length=30)
	password1 = forms.CharField(max_length=30)
	password2 = forms.CharField(max_length=30)
	avatar = forms.ImageField()

	def is_valid_(self):
		ret = self.is_valid()
		if len(User.objects.filter(username=self.cleaned_data.get('login'))) > 0:
			self.add_error('login', "This name is already taken")
			print 'name'
			ret = False
		if len(User.objects.filter(email=self.cleaned_data.get('email'))) > 0:
			self.add_error('email', "This email is already taken")
			print 'email'
			ret = False
		if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
			self.add_error('password1', "Passwords do not match")
			self.add_error('password2', "Passwords do not match")
			print 'pass'
			ret = False
		return ret

	def save_user(self):
		if self.is_valid_():
			user = User.objects.create_user(username=self.cleaned_data.get('login'),
												  email=self.cleaned_data.get('email'),
												  first_name=self.cleaned_data.get('nickName'),
												  password=self.cleaned_data.get('password1'),
												  )
			user.avatar = self.cleaned_data.get('avatar')
			user.save()
			profile = Profile(user=user)
			profile.save()
			return True
		return False


class NewQuestionForm(forms.Form):
	title = forms.CharField(label='title', max_length=200)
	text = forms.CharField(label='text')
	tags = forms.CharField(label='tags', max_length=62)


class AnswerForm(forms.Form):
	answer = forms.CharField(label='answer', max_length=1200)
