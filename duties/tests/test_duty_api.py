from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from datetime import date
from django.contrib.auth import get_user_model
from accounts.models import Profile

from ..models import Duty


User = get_user_model()


# create a client to perform requests
@pytest.fixture
def api_client():
    client = APIClient()
    return client


# create a user
@pytest.fixture
def common_user():
    user = User.objects.create_user(email="admin@admin.com", password="aqw/123456")
    return user


# create a duty
@pytest.fixture
def common_duty():
    user = User.objects.create_user(email="admin@admin.com", password="aqw/123456")
    profile = Profile.objects.create(
        user=user, first_name="test first_name", last_name="test last_name"
    )
    duty = Duty.objects.create(
        author=profile,
        title="test title",
        description="test description",
        done_status="don",
        deadline_date=date.today(),
    )
    return duty


# tests class
@pytest.mark.django_db
class TestDutyApi:

    # test that an unauthenticated user is able to read duty-list
    def test_get_duty_response_200_status(self, api_client):
        url = reverse("api-v1:duty-list")
        response = api_client.get(url)
        assert response.status_code == 200

    # test that an unauthenticated user is not able to create a duty
    def test_create_duty_response_401_status(self, api_client):
        url = reverse("api-v1:duty-list")
        data = {
            "title": "test",
            "description": "test description",
            "done_status": "don",
            "deadline_date": date.today(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    # test that an authenticated user is able to create a duty
    def test_create_duty_response_201_status(self, api_client, common_user):
        url = reverse("api-v1:duty-list")
        data = {
            "title": "test",
            "description": "test description",
            "done_status": "don",
            "deadline_date": date.today(),
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    # test that a duty would not be created with invalid data
    def test_create_duty_invalid_date_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("api-v1:duty-list")
        data = {
            "title": "test",
            "description": "test description",
            "done_status": "don",
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    # test that an unauthenticated user is able to read a duty detail
    def test_get_duty_detail_response_200_status(self, api_client, common_duty):
        url = reverse("api-v1:duty-detail", kwargs={"pk": common_duty.id})
        response = api_client.get(url)
        assert response.status_code == 200

    # test that an unauthorized user is not able to edit a duty by put method
    def test_update_duty_detail_response_401_status(self, api_client, common_duty):
        url = reverse("api-v1:duty-detail", kwargs={"pk": common_duty.id})
        data = {
            "title": "test2",
            "description": "test description2",
            "done_status": "don",
            "deadline_date": date.today(),
        }
        response = api_client.put(url, data)
        assert response.status_code == 401

    # test that an authorized user is able to edit a duty by put method
    def test_update_duty_detail_response_200_status_by_put(
        self, api_client, common_duty
    ):
        url = reverse("api-v1:duty-detail", kwargs={"pk": common_duty.id})
        data = {
            "title": "test2",
            "description": "test description2",
            "done_status": "don",
            "deadline_date": date.today(),
        }
        api_client.force_authenticate(user=common_duty.author.user)
        response = api_client.put(url, data)
        assert response.status_code == 200

    # test that an unauthorized user is not able to edit a duty by patch method
    def test_update_duty_detail_response_401_status_by_patch(
        self, api_client, common_duty
    ):
        url = reverse("api-v1:duty-detail", kwargs={"pk": common_duty.id})
        data = {
            "title": "test2",
            "description": "test description2",
        }
        response = api_client.patch(url, data)
        assert response.status_code == 401

    # test that an authorized user is able to edit a duty by patch method
    def test_update_duty_detail_response_200_status_by_patch(
        self, api_client, common_duty
    ):
        url = reverse("api-v1:duty-detail", kwargs={"pk": common_duty.id})
        data = {
            "title": "test2",
            "description": "test description2",
        }
        api_client.force_authenticate(user=common_duty.author.user)
        response = api_client.patch(url, data)
        assert response.status_code == 200

    # test that an unauthorized user is not able to delete a duty
    def test_delete_duty_detail_response_401_status(self, api_client, common_duty):
        url = reverse("api-v1:duty-detail", kwargs={"pk": common_duty.id})
        response = api_client.delete(url)
        assert response.status_code == 401

    # test that an authorized user is able to delete a duty
    def test_delete_duty_detail_response_204_status(self, api_client, common_duty):
        url = reverse("api-v1:duty-detail", kwargs={"pk": common_duty.id})
        api_client.force_login(user=common_duty.author.user)
        response = api_client.delete(url)
        assert response.status_code == 204

    # test that a created duty is displayed in duty-list
    def test_duty_list_content(self, api_client, common_duty):
        url = reverse("api-v1:duty-list")
        response = api_client.get(url)
        response_data = response.json()
        duties = response_data.get("results")
        duty_titles = [duty.get("title") for duty in duties]
        assert common_duty.title in duty_titles
