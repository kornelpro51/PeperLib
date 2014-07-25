from django.db import models

import datetime
import os


def paper_name_changer(path):

    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        thisYear = datetime.datetime.now().year
        firstdate = datetime.datetime(thisYear, 1, 1, 0, 0, 0)
        lastdate = datetime.datetime(thisYear+1, 1, 1, 0, 0, 0)
        postfix = Paper.objects.filter(created_at__gte=firstdate, created_at__lt=lastdate).count() + 1

        thisYear = str(thisYear)

        filename = '{}_{:0>3}.{}'.format(thisYear, postfix, ext)
            # return the whole path to the file
        return os.path.join(path, thisYear, filename)

    return wrapper


class Keyword(models.Model):
    keyword = models.CharField(max_length=64)

    def __unicode__(self):
        return self.keyword


class Paper(models.Model):
    title = models.CharField(max_length=255, blank=False)
    abstract = models.CharField(max_length=5000, blank=True)
    file = models.FileField(upload_to=paper_name_changer('papers'), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def file_name(self):
        return str(self.file).split('/')[-1]

    def min_abstract(self):
        if len(self.abstract) > 5:
            return self.abstract[:5] + "..."
        return self.abstract

    def author_count(self):
        #return Author.objects.filter(paper=self)[0].fullname()
        authors = Author.objects.filter(paper=self)
        if (authors.count() == 0):
            label = ""
        elif (authors.count() == 1):
            label = authors[0].fullname()
        else:
            label = authors[0].fullname() + ", ..."
        return label


class Author(models.Model):
    firstname = models.CharField(max_length=64, blank=False)
    lastname = models.CharField(max_length=64, blank=False)
    contact = models.CharField(max_length=256, blank=True)
    organization = models.CharField(max_length=256, blank=True)

    paper = models.ForeignKey(Paper, default=None, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.firstname + ' ' + self.lastname

    def fullname(self):
        return self.firstname + ' ' + self.lastname

class PaperKeyword(models.Model):
    paper = models.ForeignKey(Paper, default=None, blank=False)
    keyword = models.ForeignKey(Keyword, blank=False)


