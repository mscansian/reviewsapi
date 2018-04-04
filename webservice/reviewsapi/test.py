from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.authtoken.models import Token

from reviewsapi.models import Review


class ReviewListCreateRetrieveTests(APITestCase):
    """Test case for listing, creating and retrieving reviews"""
    def setUp(self):
        self.username = 'johndoe'
        self.email = 'john@doe.com'
        self.password = 'trustno1'
        self.user = User.objects.create_user(self.username, self.email,
                                             self.password)
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_can_get_apiroot(self):
        """Ensure the api root is configured"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_list_reviews(self):
        """Ensure we can list the reviews"""
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create_review(self):
        """Ensure we can create a review

        Criteria: Users are able to submit reviews to the API
        Criteria: Submitted reviews must include, at least, the following attributes
        """
        url = reverse('review-list')
        review = {
            "company": "SpaceX",
            "title": "My review",
            "summary": "This is the best place ever!",
            "rating": 3,
            "author": "John",
        }
        response = self.client.post(url, review)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_review_rating_higher_than_5(self):
        """Ensure we cannot create a review with a rating higher than 5

        Criteria: Rating - must be between 1 - 5
        """
        url = reverse('review-list')
        review = {
            "company": "SpaceX",
            "title": "My review",
            "summary": "This is the best place ever!",
            "rating": 6,
            "author": "John",
        }
        response = self.client.post(url, review)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_review_rating_lower_than_1(self):
        """Ensure we cannot create a review with a rating lower than 1

        Criteria: Rating - must be between 1 - 5
        """
        url = reverse('review-list')
        review = {
            "company": "SpaceX",
            "title": "My review",
            "summary": "This is the best place ever!",
            "rating": 0,
            "author": "John",
        }
        response = self.client.post(url, review)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_retrieve_review(self):
        """Ensure we can retrieve a review created by us

        Criteria: Users are able to retrieve reviews that they submitted
        """
        review_data = {
            "company": "SpaceX",
            "title": "My review",
            "summary": "This is the best place ever!",
            "rating": 3,
            "author": "John",
            "ip_addr": "127.0.0.1",
            "user": self.user,
        }
        review = Review.objects.create(**review_data)
        url = reverse('review-detail', args=(review.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_other_users_reviews(self):
        """Ensure we cannot retrieve a review created by other users

        Criteria: Users cannot see reviews submitted by other users
        """
        another_user = User.objects.create(username='anotheruser')
        review_data = {
            "company": "SpaceX",
            "title": "My review",
            "summary": "This is the best place ever!",
            "rating": 3,
            "author": "John",
            "ip_addr": "127.0.0.1",
            "user": another_user,
        }
        review = Review.objects.create(**review_data)
        url = reverse('review-detail', args=(review.pk,))
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


class ApiAuthTests(APITestCase):
    """Test case for detecting unauthenticated access to the api"""
    def test_noauth_cannot_get_apiroot(self):
        """Nobody is allowed to access the API without auth token

        Criteria: Use of the API requires a unique auth token for each user
        """
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_noauth_cannot_list_reviews(self):
        """Nobody is allowed to list reviews without proper authentication"""
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_noauth_cannot_create_review(self):
        """Nobody is allowed to create reviews without proper authentication"""
        url = reverse('review-list')
        review = {
            "company": "SpaceX",
            "title": "My review",
            "summary": "This is the best place ever!",
            "rating": 3,
            "author": "John",
        }
        response = self.client.post(url, review)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
