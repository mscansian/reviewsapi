from django.contrib import admin
from reviewsapi.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
