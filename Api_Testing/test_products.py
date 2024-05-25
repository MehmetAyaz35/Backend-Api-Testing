import pytest
import requests

BASE_URL = "http://localhost:5000" 

@pytest.fixture()
def reset_data():
    requests.get(f"{BASE_URL}/reset")
    return

@pytest.mark.status
def test_status():
    response = requests.get(f"{BASE_URL}")
    assert response.status_code == 200

@pytest.mark.read
def test_list_products():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.read
def test_list_products_with_max():
    response = requests.get(f"{BASE_URL}/products?max_price=40")
    assert len(response.json()) == 2

@pytest.mark.get
def test_get_product_detail():
    response = requests.get(f"{BASE_URL}/products/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Laptop"

@pytest.mark.get
def test_get_product_detail_404():
    response = requests.get(f"{BASE_URL}/products/4")
    assert response.status_code == 404
    assert isinstance(response.json(), dict)
    assert "message" in response.json() 

@pytest.mark.post
def test_create_product(reset_data):
    new_product = {
        "name": "Lenovo pro",
        "price": 20.0,
        "category": "Electronics",
        "specification": {
            "color": "white",
            "weight": 30.5,
            "height": 8.0,
            "length": 5.0
        },
        "stock": 5
    }
    response = requests.post(f"{BASE_URL}/products", 
                             json=new_product
                             )
    data = response.json()
    assert response.status_code == 201
    assert isinstance(data, dict)
    assert "id" in data
    assert "name" in data
    assert "price" in data
    assert "category" in data
    assert "specification" in data
    assert "stock" in data
    
    response2 = requests.get(f"{BASE_URL}/products")
    assert len(response2.json()) == 4

@pytest.mark.post
@pytest.mark.product_validation
def test_create_product_color(reset_data):
    new_product = {
        "name": "Laptop Asus Rog", 
        "price": 400.0, 
        "category": "Electronics", 
        "specification": {
            "color": "dark blue", # not allowed color
            "weight": 1.5, 
            "height": 2.0, 
            "length": 15.0},
        "description": "High performance laptop",
        "stock": 0
    }
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    assert response.status_code == 400
    assert response.json()[0]["type"] == "value_error"
    assert response.json()[0]["loc"] == [
            "specification",
            "color"
        ]
    
@pytest.mark.post
@pytest.mark.product_validation
def test_create_product_categori(reset_data):
    new_product = {
        "name": "Lenovo pro",
        "price": 20.0,
        "category": "Food", # not allowed category
        "specification": {
            "color": "blue", 
            "weight": 30.5,
            "height": 8.0,
            "length": 5.0
        },
        "stock": 5
    }
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    assert response.status_code == 400
    assert response.json()[0]["type"] == "value_error"
    assert response.json()[0]["loc"] == [
            "category"
        ]

@pytest.mark.put
def test_update_product(reset_data):
    new_product = {
        "name": "Asus Rog",
        "price": 20.0,
        "category": "Electronics",
        "specification": {
            "color": "white",
            "weight": 30.5,
            "height": 8.0,
            "length": 5.0
        },
        "stock": 5
    }
    response = requests.put(f"{BASE_URL}/products/1", 
                             json=new_product
                             )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["id"] == 1
    assert data["name"] == "Asus Rog"
    assert data["price"] == 20.0
    assert data["category"] == "Electronics"
    assert data["stock"] == 5
#  double checked   
    response2 = requests.get(f"{BASE_URL}/products/1")  
    data2 = response2.json()
    assert data2["name"] == "Asus Rog"   

@pytest.mark.put
@pytest.mark.product_validation
def test_update_product_name_length(reset_data):
    new_product = {
        "name": "A", # invalid length
        "price": 20.0,
        "category": "Electronics",
        "specification": {
            "color": "red", 
            "weight": 30.5,
            "height": 8.0,
            "length": 5.0
        },
        "stock": 5
    }
    response = requests.put(f"{BASE_URL}/products/1", 
                             json=new_product
                             )
    data = response.json()
    assert response.status_code == 400
    assert data[0]["type"] == "string_too_short"

@pytest.mark.put
def test_update_product_404(reset_data):
    new_product = {
        "name": "Asus Rog", 
        "price": 20.0,
        "category": "Electronics",
        "specification": {
            "color": "red", 
            "weight": 30.5,
            "height": 8.0,
            "length": 5.0
        },
        "stock": 5
    }
    response = requests.put(f"{BASE_URL}/products/11111111", 
                             json=new_product
                             )
    data = response.json()
    assert response.status_code == 404
    assert "error" in data


@pytest.mark.delete
def test_delete_product(reset_data):
    response = requests.delete(f"{BASE_URL}/products/2")
    assert response.status_code == 204
    response = requests.get(f"{BASE_URL}/products/2")
    assert response.status_code == 404


@pytest.mark.delete
def test_delete_product_404(reset_data):
    response = requests.delete(f"{BASE_URL}/products/11111111")
    data = response.json()
    assert response.status_code == 404
    assert "error" in data


@pytest.mark.get
def test_search_product(reset_data):
    response = requests.get(f"{BASE_URL}/products/search?search_query=Gaming Laptop")
    data = response.json()
    assert response.status_code == 200
    assert data[0]["name"] == "Gaming Laptop"
    assert data[0]["category"] == "Electronics"
    assert data[0]["id"] == 3

@pytest.mark.put
def test_product_stock_update(reset_data):
    response = requests.put(f"{BASE_URL}/products/stock_update/2?quantity=10")
    assert response.status_code == 200
    data = response.json()
    assert data["stock"] == 10

@pytest.mark.put
def test_product_stock_update_with_negative_quantity_400(reset_data):
    response = requests.put(f"{BASE_URL}/products/stock_update/2?quantity=-10") 
    assert response.status_code == 400
    data = response.json()
    assert "error" in data

@pytest.mark.put
def test_product_stock_update_invalid_id_404(reset_data):
    response = requests.put(f"{BASE_URL}/products/stock_update/999?quantity=10") 
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


@pytest.mark.post
def test_create_product_bulk(reset_data):
    new_products = {
    "products": [
        {
            "name": "Work laptop11111111",
            "price": 20.0,
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 0
        },
        {
            "name": "Work laptop22222222",
            "price": 20.0,
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 0
        }
    ]
}
    response = requests.post(f"{BASE_URL}/products/bulk", json= new_products)
    assert response.status_code == 201
    data = response.json()
    assert data[0]["id"] == 4
    assert data[0]["name"] == "Work laptop11111111" 
    assert data[0]["category"] == "Electronics" 
    assert data[1]["id"] == 5
    assert data[1]["name"] == "Work laptop22222222"
    assert data[1]["category"] == "Electronics"


@pytest.mark.post
def test_create_product_bulk_400(reset_data):
    new_products = {
    "products": [
        {
            "name": "W",            # invalid length
            "price": 20.0,
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 0
        },
        {
            "name": "Work laptop22222222",
            "price": -20.0,                # not allowed price
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 0
        }
    ]
}
    response = requests.post(f"{BASE_URL}/products/bulk", json= new_products)
    assert response.status_code == 400
    data = response.json()
    assert data[0]["type"] == "string_too_short"
    assert data[0]["loc"] == ["products", 0,"name"]
    assert data[1]["type"] == "greater_than"
    assert data[1]["loc"] == ["products", 1,"price"]
    

@pytest.mark.put
def test_update_product_bulk(reset_data):
    new_products = {
    "products": [
        {
            "id": 1,
            "description": "low performance",
            "name": "Lenovo pro",
            "price": 20.0,
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 3
        },
        {
            "id": 2,
            "description": "high performance",
            "name": "Macbook pro",
            "price": 20.0,
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 2
        }
    ]
}
    response = requests.put(f"{BASE_URL}/products/bulk_update", json= new_products)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Lenovo pro" 
    assert data[0]["category"] == "Electronics" 
    assert data[1]["id"] == 2
    assert data[1]["name"] == "Macbook pro"
    assert data[1]["category"] == "Electronics"
# double checked
    response2 = requests.get(f"{BASE_URL}/products")
    data = response2.json()
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Lenovo pro"
    assert data[1]["id"] == 2
    assert data[1]["name"] == "Macbook pro"


@pytest.mark.put
def test_update_product_bulk_not_available_id(reset_data):
    new_products = {
    "products": [
        {
            "id": 1,
            "description": "low performance",
            "name": "Lenovo pro",
            "price": 20.0,
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 3
        },
        {
            "id": 999, # not available id
            "description": "high performance",
            "name": "Macbook pro",
            "price": 20.0,
            "category": "Electronics",
            "specification": {
                "color": "white",
                "weight": 30.5,
                "height": 8.0,
                "length": 5.0
            },
            "stock": 2
        }
    ]
}
    response = requests.put(f"{BASE_URL}/products/bulk_update", json= new_products)
    assert response.status_code == 200  # Since id number 1 is valid, it is updated successfully and receives status code 200.
    data = response.json()
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Lenovo pro" 
    assert data[0]["category"] == "Electronics"   
# double checked by using get_product_detail
    response2 = requests.get(f"{BASE_URL}/products/999")
    assert response2.status_code == 404
    data = response2.json()
    assert data["message"] == "No product found"


# @pytest.mark.put
# def test_update_product_bulk_400(reset_data):
#     new_products = {
#     "products": [
#         {
#             "id": 1,
#             "description": "low performance",
#             "name": "L",    # invalid length
#             "price": 20.0,
#             "category": "Electronics",
#             "specification": {
#                 "color": "white",
#                 "weight": 30.5,
#                 "height": 8.0,
#                 "length": 5.0
#             },
#             "stock": 3
#         },
#         {
#             "id": 2,
#             "description": "high performance",
#             "name": "Macbook pro",
#             "price": -20.0,    # not allowed price
#             "category": "Electronics",
#             "specification": {
#                 "color": "white",
#                 "weight": 30.5,
#                 "height": 8.0,
#                 "length": 5.0
#             },
#             "stock": 2
#         }
#     ]
# }
#     response = requests.put(f"{BASE_URL}/products/bulk_update", json= new_products)
#     assert response.status_code == 400
#     data = response.json()
#     assert data[0]["type"] == "string_too_short"
#     assert data[0]["loc"] == ["products", 0 ,"name"]  
#     assert data[1]["type"] == "greater_than"
#     assert data[1]["loc"] == ["products", 1 ,"price"]  

# for original code
# @pytest.mark.put
# def test_update_product_bulk_400(reset_data):
#     new_products = [
#     {
#         "id": 1,
#         "name": "L",    # invalid length
#         "price": 20.0, 
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 3
#     },
#     {
#         "id": 2,     
#         "name": "Macbook pro", 
#         "price": -20.0,    # not allowed price
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 2
#     }
#     ]
#     response = requests.put(f"{BASE_URL}/products/bulk_update", json= new_products)
#     assert response.status_code == 400
#     data = response.json()
#     assert data["type"] == "string_too_short"
#     assert data["type"] == "greater_than"
    
    





# @pytest.mark.put
# def test_update_product_bulk_400(reset_data):
#     new_products = [
#     {
#         "id": 1,
#         "name": "L",    # invalid length
#         "price": 20.0, 
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 3
#     },
#     {
#         "id": 2,     
#         "name": "Macbook pro", 
#         "price": -20.0,    # not allowed price
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 2
#     }
#     ]
#     response = requests.put(f"{BASE_URL}/products/bulk_update", json= new_products)
#     assert response.status_code == 400
#     data = response.json()
#     assert data[0]["type"] == "string_too_short"
#     assert data[0]["loc"] == ["name"]  
    

# @pytest.mark.put
# def test_update_product_bulk_400(reset_data):
#     new_products = [
#     {
#         "id": 1,
#         "name": "L",    # invalid length
#         "price": 20.0, 
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 3
#     },
#     {
#         "id": 2,     
#         "name": "Macbook pro", 
#         "price": -20.0,    # not allowed price
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 2
#     }
#     ]
#     response = requests.put(f"{BASE_URL}/products/bulk_update", json= new_products)
#     assert response.status_code == 400
#     data = response.json()

#     corrected_data = []
#     for error in data["errors"]:
#         error_json = json.loads(error)
#         corrected_data.append(error_json)

#     corrected_data = {"errors": corrected_data}
#     assert corrected_data["errors"][0][0]["type"] == "string_too_short"
#     assert corrected_data["errors"][1][0]["type"] == "greater_than"
    

# # other simple solution 
# @pytest.mark.put
# def test_update_product_bulk_400(reset_data):
#     new_products = [
#     {
#         "id": 1,
#         "name": "L",    # invalid length
#         "price": 20.0, 
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 3
#     },
#     {
#         "id": 2,     
#         "name": "Macbook pro", 
#         "price": -20.0,    # not allowed price
#         "category": "Electronics", 
#         "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
#         "stock": 2
#     }
#     ]
#     response = requests.put(f"{BASE_URL}/products/bulk_update", json= new_products)
#     assert response.status_code == 400
#     data = response.json()

#     corrected_data = []
#     for error in data:
#         error_json = json.loads(error)
#         corrected_data.append(error_json)
#     assert corrected_data[0][0]["type"] == "string_too_short"
#     assert corrected_data[1][0]["type"] == "greater_than"


    
