from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^contact/$', views.ContactPage.as_view(), name='contact'),
    url(r'^about/$', views.AboutUsPage.as_view(), name='about'),
    url(r'^page/$', views.SinglePage.as_view(), name='page'),
    url(r'^article/search/$', views.SearchArticleAPIView.as_view(), name='search_article'),
    url(r'^article/$', views.SingleArticleAPIView.as_view(), name='single_article'),
    url(r'^article/all/$', views.AllArticleAPIView.as_view(), name='all_article'),
]
