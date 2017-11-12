# helloworld/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from helloworld import views
from . import search,searchpost
urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
url(r'^search$', search.search),
url(r'^search_form$', search.search_form),
url(r'^search-post$', searchpost.search_post),
]
