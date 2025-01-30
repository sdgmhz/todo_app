import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# create a client to perform requests
@pytest.fixture
def api_client():
    return APIClient()


# create valid data for user registration
@pytest.fixture
def valid_registration_data():
    return {
        "email": "test10@test.com",
        "password": "ax/1234567",
        "password1": "ax/1234567",
    }


# create a verified user
@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="common_user@commonuser.com", password="ax/1234567", is_verified=True
    )
    return user


# create a not verified user
@pytest.fixture
def common_user_not_verified():
    user = User.objects.create_user(
        email="common_user_not_verified@commonuser.com",
        password="ax/1234567",
    )
    return user


# create token for a verified user
@pytest.fixture
def get_tokens_for_user(common_user):
    refresh = RefreshToken.for_user(common_user)
    return str(refresh.access_token)


# create token for a  not verified user
@pytest.fixture
def get_tokens_for_not_verified_user(common_user_not_verified):
    refresh = RefreshToken.for_user(common_user_not_verified)
    return str(refresh.access_token)


@pytest.mark.django_db
class TestAccountsApi:

    # test user registration with valid data and check if the user email is in response
    def test_user_registration_with_valid_data_201_status(
        self, api_client, valid_registration_data
    ):
        url = reverse("registration")
        response = api_client.post(url, valid_registration_data)
        assert response.status_code == 201
        assert "email" in response.data

    # test user registration with invalid data
    def test_user_registration_with_invalid_data_400_status(self, api_client):
        url = reverse("registration")
        invalid_data = {"email": "invalid_email", "password": "short"}
        response = api_client.post(url, invalid_data)
        assert response.status_code == 400

    # test change password with valid data
    def test_change_password_with_valid_data_200_status(self, api_client, common_user):
        url = reverse("change-password")
        data = {
            "old_password": "ax/1234567",
            "new_password": "com/newpass1234567",
            "new_password1": "com/newpass1234567",
        }
        api_client.force_login(user=common_user)
        response = api_client.put(url, data)
        assert response.status_code == 200
        assert "password changed successfully" in response.data["detail"]

    # test change password with invalid data
    def test_change_password_with_invalid_data_400_status(
        self, api_client, common_user
    ):
        url = reverse("change-password")
        data = {
            "old_password": "wrong_oldpass",
            "new_password": "com/newpass1234567",
            "new_password1": "com/newpass1234567",
        }
        api_client.force_login(user=common_user)
        response = api_client.put(url, data)
        assert response.status_code == 400
        assert "old password is wrong" in response.data["detail"]

    # test obtain token with valid login data and the existence of token in response
    def test_token_login_with_valid_data_200_status(self, api_client, common_user):
        url = reverse("token-login")
        data = {"email": common_user.email, "password": "ax/1234567"}
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert "token" in response.data

    # test obtain token with invalid login data
    def test_token_login_with_valid_data_400_status(self, api_client, common_user):
        url = reverse("token-login")
        data = {"email": common_user.email, "password": "axs/1234567"}
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert "token" not in response.data

    # test discard a token for logged in user
    def test_token_logout_discard_token_204_status(self, api_client, common_user):
        # first obtain token for the user
        url_login = reverse("token-login")
        data = {"email": common_user.email, "password": "ax/1234567"}
        response = api_client.post(url_login, data)
        # now check discarding the token
        url = reverse("token-logout")
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url)
        assert response.status_code == 204

    # test discard a token for unauthenticated user
    def test_token_logout_discard_token_401_status(self, api_client, common_user):
        # first obtain token for the user
        url_login = reverse("token-login")
        data = {"email": common_user.email, "password": "ax/1234567"}
        response = api_client.post(url_login, data)
        # now check discarding the token
        url = reverse("token-logout")
        response = api_client.post(url)
        assert response.status_code == 401

    # test activation of a new user with valid token
    def test_user_activation_with_valid_data_200_status(
        self, api_client, get_tokens_for_not_verified_user
    ):
        token = get_tokens_for_not_verified_user
        url = reverse("activation", kwargs={"token": token})
        response = api_client.get(url)
        assert response.status_code == 200
        assert (
            "our account has been verified and activated successfully"
            in response.data["detail"]
        )

    # test activation of a new user with invalid token
    def test_user_activation_with_invalid_data_400_status(
        self, api_client, get_tokens_for_not_verified_user
    ):
        token = get_tokens_for_not_verified_user + "invaliddata"
        url = reverse("activation", kwargs={"token": token})
        response = api_client.get(url)
        assert response.status_code == 400
        assert "token is invalid" in response.data["detail"]

    # test resend activation with a not verified account
    def test_user_resend_activation_with_valid_email_not_verified_200_status(
        self, api_client, common_user_not_verified
    ):
        url = reverse("activation-resend")
        data = {"email": common_user_not_verified.email}
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert "user activation email resend successfully" in response.data["detail"]

    # test resend activation with a verified account
    def test_user_resend_activation_with_valid_email_verified_406_status(
        self, api_client, common_user
    ):
        url = reverse("activation-resend")
        data = {"email": common_user.email}
        response = api_client.post(url, data)
        assert response.status_code == 406
        assert "your account has already been verified" in response.data["detail"]

    # test request a password reset data for a verified user
    def test_password_reset_with_valid_data_200_status(self, api_client, common_user):
        url = reverse("password-reset")
        data = {"email": common_user.email}
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert (
            "If there is an account with this email, we will send an password reset link for you. Check your inbox!"
            in response.data["detail"]
        )

    # test request a password reset data for a not verified user
    def test_password_reset_with_invalid_data_not_verified_user_400_status(
        self, api_client, common_user_not_verified
    ):
        url = reverse("password-reset")
        data = {"email": common_user_not_verified.email}
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert (
            "Your account is not verified. First you should request for user verification. "
            in response.data["detail"]
        )

    # test password reset confirm
    def test_password_reset_confirm_valid_data_200_status(
        self, api_client, get_tokens_for_user
    ):
        token = get_tokens_for_user
        print(token)
        url = reverse("password-reset-confirm", kwargs={"token": token})
        data = {
            "new_password": "asd/1234567",
            "new_password1": "asd/1234567",
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        assert "password reset successfully for user" in response.data["detail"]
