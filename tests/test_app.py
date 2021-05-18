from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

data = {
    'breed': 'Ragdoll',
    'location_of_origin': 'United States',
    'coat_length': 4,
    'body_type': 'Medium',
    'pattern': 'Chocolate Point'
}


# Validation of POST Request
def test_add_cat():
    response = client.post("/cats", json=data)
    assert response.status_code == 201
    assert response.json() == data


# Validation of GET Request
def test_get_cats():
    response = client.get("/cats", json=data)
    assert response.status_code == 200
    assert data in response.json()


# Validation of unique breed
def test_add_cat_same_breed():
    response = client.post("/cats", json=data)
    assert response.status_code == 406
    assert response.json() == {'detail': 'Breed already exists.'}


# Validation of positive integer
def test_add_cat_invalid_coat_length():
    response = client.post("/cats", json={'breed': 'Sphynx',
                                          'location_of_origin': 'United States',
                                          'coat_length': -5,
                                          'body_type': 'Medium',
                                          'pattern': 'Chocolate Point'})
    assert response.status_code == 406
    assert response.json() == {'detail': 'Coat length must be equal or greater than 0.'}


# Validation if body size is inside given list
def test_add_cat_invalid_body_size():
    response = client.post("/cats", json={'breed': 'American Shorthair',
                                          'location_of_origin': 'United States',
                                          'coat_length': 1,
                                          'body_type': 'Super Small Cat',
                                          'pattern': 'Chocolate Point'})
    assert response.status_code == 406
    assert response.json() == {'detail': 'Body type must be Small, Medium or Large'}


# Validation of PATCH request
def test_update_cat():
    response = client.patch("/cats/Ragdoll", json={'breed': 'Ragdoll',
                                                   'location_of_origin': 'Russia',
                                                   'coat_length': 5,
                                                   'body_type': 'Small',
                                                   'pattern': 'Black And White'})
    assert response.status_code == 202
    assert response.json() == {'breed': 'Ragdoll',
                               'location_of_origin': 'Russia',
                               'coat_length': 5,
                               'body_type': 'Small',
                               'pattern': 'Black And White'}


# Validation if cat exists
def test_update_cat_not_found():
    response = client.patch("/cats/Unknown", json={'breed': 'Unknown',
                                                   'location_of_origin': 'United States',
                                                   'coat_length': 5,
                                                   'body_type': 'Small',
                                                   'pattern': 'Black And White'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Cat not found.'}


# Validation of positive integer
def test_update_cat_invalid_coat_length():
    response = client.patch("/cats/Ragdoll", json={'breed': 'Ragdoll',
                                                   'location_of_origin': 'Russia',
                                                   'coat_length': -5,
                                                   'body_type': 'Small',
                                                   'pattern': 'Black And White'})
    assert response.status_code == 406
    assert response.json() == {'detail': 'Coat length must be equal or greater than 0.'}


# Validation if body size is inside given list
def test_update_cat_invalid_body_type():
    response = client.patch("/cats/Ragdoll", json={'breed': 'Ragdoll',
                                                   'location_of_origin': 'Russia',
                                                   'coat_length': 5,
                                                   'body_type': 'Super Large',
                                                   'pattern': 'Black And White'})
    assert response.status_code == 406
    assert response.json() == {'detail': 'Body type must be Small, Medium or Large'}


# Validation of DELETE request
def test_remove_cat():
    response = client.delete("/cats/Ragdoll")
    assert response.status_code == 200
