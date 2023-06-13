from client import RestfulBookerClient
import allure

client = RestfulBookerClient()
client.authorize("admin111@gm.com", "password123")

# POST /api/AuthAccount/Login endpoint tests

@allure.story('The login is successful with the correct creds')
def test_successful_login():
    data = {
        "email": "admin111@gm.com",
        "password": "password123"
    }
    response = client.perform_post_request("/api/AuthAccount/Login", data)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["message"] == "success"

@allure.story('The login is unsuccessful with the incorrect creds')
def test_unsuccessful_login():
    data = {
        "email": "admin111@gmcom",
        "password": "password123"
    }
    response = client.perform_post_request("/api/AuthAccount/Login", data)
    response_body = response.json()

    assert response.status_code == 200 # IMHO should not be 200 as designed there
    assert response_body["message"] == "invalid username or password"

@allure.story('The login is unsuccessful with the empty creds')
def test_unsuccessful_empty_login():
    data = {
        "email": "",
        "password": ""
    }
    response = client.perform_post_request("/api/AuthAccount/Login", data)
    response_body = response.json()

    assert response.status_code == 400
    assert response_body["Message"] == "The request is invalid."