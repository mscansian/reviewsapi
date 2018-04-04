from rest_framework.routers import DefaultRouter
from reviewsapi.views import ReviewsViewSet


router = DefaultRouter()
router.register(r'reviews', ReviewsViewSet, base_name='review')
urlpatterns = router.urls
