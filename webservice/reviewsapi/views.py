from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin

from reviewsapi.serializers import ReviewSerializer
from reviewsapi.models import Review


class ReviewsViewSet(CreateModelMixin,
                     RetrieveModelMixin,
                     ListModelMixin,
                     GenericViewSet):
    """DRF Viewset for listing, retrieving and creating reviews"""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Inject the IP address and user into the serializer
        ip_addr = self.request.META.get('REMOTE_ADDR')
        serializer.validated_data['ip_addr'] = ip_addr
        serializer.validated_data['user'] = self.request.user
        super().perform_create(serializer)
