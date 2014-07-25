from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse

from models import *
from forms import *

import json


class BookListView(TemplateView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        return {'papers': Paper.objects.all()}


class BookCreateView(TemplateView):
    template_name = "create.html"


class PaperView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('ahaha - GET')

    def post(self, request, *args, **kwargs):
        #if (request.post.title):

        form = PaperForm(request.POST, request.FILES)
        if not form.is_valid():
            if request.is_ajax():
                return HttpResponse('error')
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
            return HttpResponse(json.dumps({success: true}), content_type="application/json")
        return HttpResponseRedirect(reverse('book_create_view'))