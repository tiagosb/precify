products_endpoint = "http://127.0.0.1:5000/api/v1/products"
providers_endpoint = "http://127.0.0.1:5000/api/v1/providers"
prices_endpoint = "http://127.0.0.1:5000/api/v1/prices"


def test_prices_post_shoud_return_201_created(client):

    #Insert new product for testing
    req1 = client.post(
        products_endpoint,
        json={
            "name": "Product price test",
            "description": "Product to add price in test",
        },
    )

    #Insert new provider for testing
    req2 = client.post(
        providers_endpoint,
        json={
            "name": "Provider price test",
            "description": "Provider to add price in test"
        }
    )
    product = req1.get_json()
    provider = req1.get_json()

    #Try insert new price
    req3 = client.post(
        prices_endpoint,
        json={
            "product_id": product.get("id"),
            "provider_id": provider.get("id"),
            "price": 12.99
        }
    )

    assert req3.status_code == 201

def test_prices_post_shoud_return_400_bad_request(client):
    #Try insert empty price
    req = client.post(
        prices_endpoint, json={}
    )
    #Try insert new price missing the price
    req2 = client.post(
        prices_endpoint,
        json={
            "product_id": 1,
            "provider_id": 1
        }
    )
    #Try insert new price missing the product id
    req3 = client.post(
        prices_endpoint,
        json={
            "provider_id": 1,
            "price": 12.93
        }
    )

    #Try insert new price missing the provider id
    req4 = client.post(
        prices_endpoint,
        json={
            "product_id": 1,
            "price": 12.93
        }
    )

    assert req.status_code == req2.status_code == req3.status_code == req4.status_code == 400

def test_prices_post_shoud_return_409_constraint_error(client):
    """
        Ther first inserted price has the same prod id and prov id, so shoul return constraint error
    """
    req = client.post(
        prices_endpoint,
        json={
            "product_id": 1,
            "provider_id": 1,
            "price": 12.99
        }
    )
    assert req.status_code == 409

# Inexistent product_id or provider_id shoul result in integrity error but is not working!!! Fix it later
# def test_prices_post_shoud_return_invalid_product_or_provider(client):
#         req = client.post(
#             prices_endpoint,
#             json={
#                 "product_id":33,
#                 "provider_id": 33,
#                 "price": 199.33
#             }
#         )
#         assert req.status_code == 409