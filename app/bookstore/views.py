from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from django.core import serializers

from models import *
from forms import *

import json


class BookListView(TemplateView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        return {'papers': Paper.objects.all()}


class BookCreateView(TemplateView):
    template_name = "create.html"

    def get_context_data(self, **kwargs):
        return {'keywords': serializers.serialize('json', Keyword.objects.all())}


class BookDetailView(TemplateView):
    template_name = "edit.html"

    def get_context_data(self, **kwargs):
        paper_id = kwargs.get('paperid')
        #return {'papers': Paper.objects.all()}
        return {'paper': Paper.objects.get(id=paper_id), 'keywords': PaperKeyword.objects.filter(paper_id=paper_id), 'authors': Author.objects.filter(paper_id=paper_id)}


class PaperView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('ahaha - GET')

    def post(self, request, *args, **kwargs):
        #if (request.post.title):

        form = PaperForm(request.POST, request.FILES)
        if not form.is_valid():
            if request.is_ajax():
                return HttpResponse(json.dumps({'success': False}), content_type="application/json")
            else:
                return HttpResponseRedirect(reverse('book_create_view'))
        form.save()

        keywords = json.loads(request.POST.get('keywords'))
        authors = json.loads(request.POST.get('authors'))

        for k in keywords:
            paperkeyword = PaperKeyword(
                paper=form.instance,
                keyword=Keyword.objects.get(id=k),
            )
            paperkeyword.save()
        for a in authors:
            author = Author(
                firstname=a.get('firstname'),
                lastname=a.get('lastname'),
                contact=a.get('contact'),
                organization=a.get('organization'),
                paper=form.instance,
            )
            author.save()
        if request.is_ajax():
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        return HttpResponseRedirect(reverse('book_create_view'))


class KeywordView(View):

    def get(self, request, *args, **kwargs):
        result = []
        for k in Keyword.objects.all():
            result.append({
                'id': k.id,
                'name': k.keyword
            })
        return HttpResponse(json.dumps(result), content_type="application/json")