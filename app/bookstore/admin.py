from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Keyword)
admin.site.register(Paper)
admin.site.register(Author)
admin.site.register(PaperKeyword)
