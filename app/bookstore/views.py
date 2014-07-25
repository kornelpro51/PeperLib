from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView, View

# from bookstore.models import Book

class BookListView(TemplateView):
    template_name = "list.html"


class BookCreateView(TemplateView):
    template_name = "create.html"


class PaperView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('ahaha - GET')

    def post(self, request, *args, **kwargs):
        return HttpResponse('ahaha')