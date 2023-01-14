import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import Profile


# Create your models here.


def year_choices():
    return [(r, r) for r in range(1984, datetime.date.today().year + 1)]


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def current_year():
    return datetime.date.today().year


CHOICES = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)


class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Manga(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255)
    synopsis = models.TextField(null=False, blank=True)
    year = models.IntegerField('year', validators=[MinValueValidator(1984), max_value_current_year])
    main_photo = models.ImageField(null=True)
    genre = models.ManyToManyField(Genre, related_name='manga_genre')
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(null=True, blank=False)
    stars = models.IntegerField(default=5, choices=CHOICES)
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_query_name='review', null=True)
