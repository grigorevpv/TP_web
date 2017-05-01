from django import forms


class LoginForm(forms.Form):
	login = forms.CharField(label='Login', max_length=100, help_text='Enter your login...')
	password = forms.CharField(label='Login', max_length=100, widget=forms.PasswordInput())


class NewQuestionForm(forms.Form):
	title = forms.CharField()
	text = forms.CharField()
	tags = forms.CharField()


class AnswerForm(forms.Form):
	answer = forms.CharField(label='answer', max_length=1200)

