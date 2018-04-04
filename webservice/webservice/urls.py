from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', views.obtain_auth_token),
    url(r'^', include('reviewsapi.urls')),
]
