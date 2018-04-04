from rest_framework import serializers
from reviewsapi.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Review DRF serializer"""
    class Meta:
        model = Review
        fields = ('id', 'company', 'title', 'summary', 'rating',
                  'author', 'ip_addr', 'created')
        read_only_fields = ('ip_addr', 'created')
