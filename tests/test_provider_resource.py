providers_endpoint = "http://127.0.0.1:5000/api/v1/providers"


def test_providers_get_should_return_200_ok(client):
    """
    Return providers in database
    """
    req = client.get(providers_endpoint, json={})
    assert req.status_code == 200


def test_providers_get_shoud_return_404_page_or_provider_not_found(client):
    req = client.get(providers_endpoint, json={"page": 10})
    req2 = client.get(providers_endpoint, json={"id": 10})
    assert req.status_code == 404
    assert req2.status_code == 404


def test_providers_post_should_return_201_created(client):
    """
    Add a new provider
    """
    req = client.post(
        providers_endpoint,
        json={"name": "Provider test", "description": "This is the provider from test"},
    )
    assert req.status_code == 201


def test_providers_get_shoud_return_provider_data_by_id(client):
    req = client.post(
        providers_endpoint,
        json={
            "name": "Provider to search",
            "description": "Search this provider by id",
        },
    )

    provider = req.get_json()

    req2 = client.get(providers_endpoint, json={"id": provider.get("id")})

    assert req2.status_code == 200
    assert req2.get_json().get("name") == provider.get("name")
    assert req2.get_json().get("description") == provider.get("description")


def test_providers_post_should_return_409_duplicated(client):
    """
    Duplicated provider. Each provider should have a unique name.
    """
    req = client.post(
        providers_endpoint,
        json={"name": "Provider test", "description": "This is the provider from test"},
    )
    assert req.status_code == 409
    assert "should be unique" in req.get_json().get("message")


def test_providers_post_should_return_400_bad_request(client):
    req1 = client.post(providers_endpoint, json={})
    req2 = client.post(providers_endpoint, json={"name": "New provider Test"})
    req3 = client.post(
        providers_endpoint, json={"description": "This is a test provider"}
    )
    assert (
        req1.status_code == 400 and req2.status_code == 400 and req3.status_code == 400
    )

def test_providers_delete_should_return_404_not_found(client):
    req = client.delete(providers_endpoint, json={"id": 100})
    assert "not found" in req.get_json().get("message")
    assert req.status_code == 404

def test_providers_delete_should_return_204_deleted(client):
    req = client.post(
        providers_endpoint,
        json={"name": "Delete provider test", "description": "This provider will be deleted"},
    )
    provider_id = req.get_json().get("id")
    req_del = client.delete(providers_endpoint, json={"id": provider_id})
    assert req_del.status_code == 204

def test_providers_put_should_return_400_bad_request(client):
    """
    Providers put missing provider data to change should return a bad request code
    """
    req1 = client.put(providers_endpoint, json={})
    req2 = client.put(providers_endpoint, json={"id": 1})
    assert req1.status_code == 400 and req2.status_code == 400


def test_provider_put_should_return_404_not_found(client):
    """
    If provider with the id doesn't exist should return 404 status code
    """
    req = client.put(
        providers_endpoint,
        json={
            "id": 1000,
            "name": "Provider inexistent",
            "description": "This provider doesn't exist.",
        },
    )
    assert req.status_code == 404

def test_provider_put_should_return_200_ok_altered(client):
    req1 = client.post(
        providers_endpoint,
        json={
            "name": "Provider to update",
            "description": "This provider will be updated by testing",
        },
    )
    provider = req1.get_json()

    req2 = client.put(
        providers_endpoint,
        json={
            "id": provider.get("id"),
            "name": provider.get("name") + "x",
            "description": provider.get("description") + "x",
        },
    )
    assert req2.status_code == 200
    assert "x" in req2.get_json().get("name")
    assert "x" in req2.get_json().get("description")

def test_providers_put_should_return_409_duplicated(client):
    """
    Insert two providers then try update the second one to be equals the first
    """
    req = client.post(
        providers_endpoint,
        json={
            "name": "provider for testing 1",
            "description": "provider for testing 1 will be duplicated in update",
        },
    )

    req2 = client.post(
        providers_endpoint,
        json={
            "name": "provider for testing 2",
            "description": "provider for testing 2 will be duplicated in update",
        },
    )
    assert req.status_code == 201 and req2.status_code == 201

    provider1 = req.get_json()
    provider2 = req2.get_json()

    req3 = client.put(
        providers_endpoint,
        json={
            "id": provider2.get("id"),
            "name": provider1.get("name"),
            "description": provider1.get("description"),
        },
    )

    assert req3.status_code == 409
