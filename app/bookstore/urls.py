from django.conf.urls import patterns, include, url

from app.bookstore.views import BookListView, BookCreateView, PaperView

urlpatterns = patterns(
    'app.bookstore.views',

    url(r'^create/$', BookCreateView.as_view(), name='book_create_view'),
    url(r'^$', BookListView.as_view(), name='book_list_view'),
    url(r'^api/v1/paper/$', PaperView.as_view(), name='book_create'),
)
