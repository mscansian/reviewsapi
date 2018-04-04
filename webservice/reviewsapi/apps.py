from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ReviewsAPIConfig(AppConfig):
    name = "reviewsapi"
    verbose_name = _("Reviews API")
