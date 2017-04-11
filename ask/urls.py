from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^hello/', views.hello, name='hello'),
    url(r'^hot/', views.hot, name='hot'),
    url(r'^questions/', views.questions_list, name='questions'),
    url(r'^tag/(?P<tagName>[A-Za-z0-9]+)/', views.tag, name='tag'),
    url(r'^question/(?P<question>[0-9]+)/$', views.question, name='question'),
    url(r'^login/', views.login, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^get_post/', views.get_post, name='get_post'),
    url(r'^list/(?P<list>[0-9]+)/$', views.list, name='list'),
]