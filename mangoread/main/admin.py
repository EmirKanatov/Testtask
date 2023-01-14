from django.contrib import admin

from main.models import Manga, Review, Genre

# Register your models here.
admin.site.register(Manga)
admin.site.register(Genre)
admin.site.register(Review)
