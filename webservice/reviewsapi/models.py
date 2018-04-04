from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Review(models.Model):
    """Review database model"""
    company = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=1e4)
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])
    author = models.CharField(max_length=64)

    # Metadata
    ip_addr = models.GenericIPAddressField()
    created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey("auth.User", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title} @ {self.company}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """post_save signal responsible for creating an auth token for each user"""
    if created:
        Token.objects.create(user=instance)
