from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q

from .models import Book, Review


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/books_list.html"
    login_url = "account_login"


class BookDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"
    login_url = "account_login"
    permission_required = "books.special_status"
    queryset = Book.objects.all().prefetch_related('reviews__author', )


class SearchResultsListView(ListView):
    model = Book, Review
    context_object_name = "search_result"
    template_name = "books/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        search_result_book = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

        search_result_review = Review.objects.filter(review__icontains=query)


        return [search_result_book, search_result_review]
