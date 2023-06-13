from client import RestfulBookerClient
import allure

client = RestfulBookerClient()
client.authorize("admin111@gm.com", "password123")

@allure.step
def get_tourist_id(tourist_email):
    response = client.perform_get_request("/api/Tourist")
    response_body = response.json()

    tourist_id = 0
    for item in response_body["data"]:
        if item["tourist_email"] == tourist_email:
            tourist_id = item["id"]
    return tourist_id

@allure.step
def delete_tourist(tourist_email):
    tourist_id = get_tourist_id(tourist_email)

    client.perform_delete_request(f"/api/Tourist/{tourist_id}")


# "GET /api/Tourist/{id} endpoint tests"

@allure.story('The tourist data is being returned')
def test_get_tourist():
    response = client.perform_get_request("/api/Tourist")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["data"][0]["id"] is not None
    assert isinstance(response_body["data"], list)


@allure.story('The new tourist is being correctly created')
def test_create_tourist():
    new_tourist = {
        "id": 100500,
        "tourist_name": "H",
        "tourist_email": "nnn@gm.com",
        "tourist_location": "G",
        "createdat": "2023-06-12T20:25:04.282Z"
}

    response = client.perform_post_request("/api/Tourist", new_tourist)
    response_body = response.json()

    assert response.status_code == 201
    assert response_body["tourist_name"] == "H"
    assert response_body["tourist_email"] == "nnn@gm.com"


@allure.story('The tourist data can be retrieved by an id')
def test_get_tourist_by_id():
    tourist_id = get_tourist_id("nn@gm.com")
    response = client.perform_get_request(f"/api/Tourist/{tourist_id}")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["tourist_name"] is not None
    assert response_body["tourist_email"] is not None

@allure.story('The tourist is not found')
def test_get_inexistent_tourist():
    tourist_id = 90000000
    response = client.perform_get_request(f"/api/Tourist/{tourist_id}")

    assert response.status_code == 404


