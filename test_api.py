from client import RestfulBookerClient

client = RestfulBookerClient()
client.authorize("admin111@gm.com", "password123")

def get_tourist_id(tourist_email):
    response = client.perform_get_request("/api/Tourist")
    response_body = response.json()

    tourist_id = 0
    for item in response_body["data"]:
        if item["tourist_email"] == tourist_email:
            tourist_id = item["id"]
    return tourist_id

def delete_tourist(tourist_email):
    tourist_id = get_tourist_id(tourist_email)

    client.perform_delete_request(f"/api/Tourist/{tourist_id}")

# GET /api/Tourist/{id} endpoint tests
def test_get_tourist():
    response = client.perform_get_request("/api/Tourist")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["data"][0]["id"] is not None
    assert isinstance(response_body["data"], list)


def test_create_tourist():
    new_tourist = {
        "id": 100500,
        "tourist_name": "H",
        "tourist_email": "nn@gm.com",
        "tourist_location": "G",
        "createdat": "2023-06-12T20:25:04.282Z"
}

    response = client.perform_post_request("/api/Tourist", new_tourist)
    response_body = response.json()

    assert response.status_code == 201
    assert response_body["tourist_name"] == "H"
    assert response_body["tourist_email"] == "nn@gm.com"


def test_get_tourist_by_id():
    tourist_id = get_tourist_id("nn@gm.com")
    response = client.perform_get_request(f"/api/Tourist/{tourist_id}")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["tourist_name"] is not None
    assert response_body["tourist_email"] is not None

def test_get_inexistent_tourist():
    tourist_id = 90000000
    response = client.perform_get_request(f"/api/Tourist/{tourist_id}")

    assert response.status_code == 404


# POST /api/AuthAccount/Login endpoint tests

def test_successful_login():
    data = {
        "email": "admin111@gm.com",
        "password": "password123"
    }
    response = client.perform_post_request("/api/AuthAccount/Login", data)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["message"] == "success"

def test_unsuccessful_login():
    data = {
        "email": "admin111@gmcom",
        "password": "password123"
    }
    response = client.perform_post_request("/api/AuthAccount/Login", data)
    response_body = response.json()

    assert response.status_code == 200 # IMHO should not be 200 as designed there
    assert response_body["message"] == "invalid username or password"

def test_unsuccessful_empty_login():
    data = {
        "email": "",
        "password": ""
    }
    response = client.perform_post_request("/api/AuthAccount/Login", data)
    response_body = response.json()

    assert response.status_code == 400
    assert response_body["Message"] == "The request is invalid."