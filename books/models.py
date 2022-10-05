import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
      return reverse("book_detail", args=[str(self.id)])


class Review(models.Model):
    related_name = "reviews"

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name=related_name,
    )
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name=related_name
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        review = f'{self.review[:20]} ..' if len(self.review) > 20 \
            else self.review
        return f'"{review}" of {self.book} by {self.author}'
