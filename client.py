import requests
import allure


class RestfulBookerClient:
    BASE_URL = "http://restapi.adequateshop.com"

    def __init__(self, token=None):
        self.token = token

    @allure.step
    def authorize(self, username, password):
        data = {
            "email": username,
            "password": password
        }
        response = self.perform_post_request("/api/AuthAccount/Login", data)
        if response.status_code == 200:
            self.token = response.json()["data"]["Token"]
        else:
            raise Exception(f"Authorization failed: {response.status_code}")
        return response

    @allure.step
    def perform_get_request(self, endpoint):
        url = self.BASE_URL + endpoint
        response = requests.get(url)
        return response

    @allure.step
    def perform_post_request(self, endpoint, data):
        url = self.BASE_URL + endpoint
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Cookie"] = f"token={self.token}"
        response = requests.post(url, json=data, headers=headers)
        return response

    @allure.step
    def perform_put_request(self, endpoint, data):
        url = self.BASE_URL + endpoint
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Cookie"] = f"token={self.token}"
        response = requests.put(url, json=data, headers=headers)
        return response

    @allure.step
    def perform_delete_request(self, endpoint, data):
        url = self.BASE_URL + endpoint
        response = requests.delete(url)
        return response