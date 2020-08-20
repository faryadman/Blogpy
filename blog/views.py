from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import stringfilter
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.template import loader
from .models import *
from taggit.models import Tag
from django.db.models import Count


class IndexPage(TemplateView):
    def get(self, request, **kwargs):
        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')

        # for pagination
        paginator = Paginator(all_articles, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # for categories
        all_categories=Category.objects.all()

        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })
        promote_data = []
        all_promote_article = Article.objects.filter(promote=True)
        for promote_article in all_promote_article:
            promote_data.append({
                'category': promote_article.category.title,
                'title': promote_article.title,
                'author': promote_article.author.user.first_name + ' ' + promote_article.author.user.last_name,
                'avatar': promote_article.author.avatar.url if promote_article.author.avatar else None,
                'cover': promote_article.cover.url if promote_article.cover else None,
                'created_at': promote_article.created_at.date(),
            })

        context = {
            'article_data': article_data,
            'promote_article_data': promote_data,
            'page_obj': page_obj,
            'all_categories': all_categories,
        }
        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = 'page-contact.html'


class AboutUsPage(TemplateView):
    template_name = 'page-about.html'


class SinglePage(TemplateView):
    def get(self, request, **kwargs):
        article_data = []

        # for pagination
        page_number = request.GET.get('page')
        print(page_number)
        all_articles = Article.objects.filter(pk=page_number)
        common_tags = Article.tag.most_common()[:5]

        for article in all_articles:
            article_data.append({
                "title": article.title,
                "cover": article.cover.url if article.cover else None,
                "content": article.content,
                "created_at": article.created_at,
                "category": article.category.title,
                "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                "author_avatar": article.author.avatar.url if article.author.avatar else None,
                "author_description": article.author.description,
                "tags": article.tag.most_common(),
                "promote": article.promote,
            })
        context = {
            'page_article_data': article_data,
        }
        return render(request, 'single-standard.html', context)


class AllArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            all_article = Article.objects.all().order_by('-created_at')
            data = []
            for article in all_article:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                    "promote": article.promote,
                })
                return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal server error , we'll check it later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleArticleAPIView(APIView):

    def get(self, request, format=None):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serilized_data = serializers.SingleArticleSerializer(article, many=True)
            data = serilized_data.data

            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal server error , we'll check it later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchArticleAPIView(APIView):

    def get(self, request, format=None):
        try:
            from django.db.models import Q

            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            data = []
            for article in articles:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                    "promote": article.promote,
                })
                return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal server error , we'll check it later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
