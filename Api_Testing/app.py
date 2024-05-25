from flask import Flask, request
from pydantic import ValidationError
from schemas import ProductSchema, BulkProductSchema


app = Flask(__name__)

# Some data for products
products = [
    {
        "id": 1, 
        "name": "Laptop", 
        "price": 800.0, 
        "category": "Electronics", 
        "specification": {"color": "black", "weight": 1.5, "height": 2.0, "length": 15.0},
        "description": "High performance laptop",
        "stock": 0
    },
    {
        "id": 2, 
        "name": "T-Shirt", 
        "price": 20.0, 
        "category": "Clothing", 
        "specification": {"color": "white", "weight": 0.2, "height": 1.0, "length": 5.0},
        "description": "Cotton t-shirt",
        "stock": 2
    },
    {
        "id": 3, 
        "name": "Gaming Laptop", 
        "price": 20.0, 
        "category": "Electronics", 
        "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
        "description": "Cool gaming laptop",
        "stock": 4
    }
]

def find_product_by_id(product_id):
    """
    Will find a product based on a product id
    """
    for product in products:
        if product["id"] == product_id:
            return product
    return None



def get_next_id(data: list):
    """
    Don't touch this
    """
    if not data:
        return 1
    return max(d['id'] for d in data) + 1
    

@app.after_request
def add_header(response):
    """
    Don't touch this
    """
    response.headers['Content-Type'] = 'application/json'
    return response

@app.get("/reset")
def reset_products():
    global products
    products = [
    {
        "id": 1, 
        "name": "Laptop", 
        "price": 800.0, 
        "category": "Electronics", 
        "specification": {"color": "black", "weight": 1.5, "height": 2.0, "length": 15.0},
        "description": "High performance laptop",
        "stock": 0
    },
    {
        "id": 2, 
        "name": "T-Shirt", 
        "price": 20.0, 
        "category": "Clothing", 
        "specification": {"color": "white", "weight": 0.2, "height": 1.0, "length": 5.0},
        "description": "Cotton t-shirt",
        "stock": 2
    },
    {
        "id": 3, 
        "name": "Gaming Laptop", 
        "price": 20.0, 
        "category": "Electronics", 
        "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
        "description": "Cool gaming laptop",
        "stock": 4
    }
]
    return {}, 200


@app.route("/")
def status():
    """
    ---- G -----
    Returns 200 OK if API is online
    """
    return {"message": "ok"}, 200

@app.route("/products", methods=["GET"])
def list_products():
    """
    ---- G -----
    Lists all products
    Can filter using a max_price query parameter
    """
    max_price = request.args.get("max_price", type=float)
    filtered_products = []
    
    if max_price:
        for product in products:
            if product["price"] <= max_price:
                filtered_products.append(product)
        return filtered_products, 200
        
    return products, 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product_detail(product_id):
    """
    ---- G -----
    Returns a product based on a product id
    """
    product = find_product_by_id(product_id)
    if product:
        return product, 200
    return {"message": "No product found"}, 404

@app.route("/products", methods=["POST"])
def create_product():
    """
    ---- G -----
    Creates a product
    Example JSON input:
    {
        "id": 1,
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
    """
    product_data = request.get_json()
    try:
        result = ProductSchema(**product_data)
        product = result.model_dump()
    except ValidationError as e:
        return e.json(), 400
   
    product["id"] = get_next_id(products)
    products.append(product)
    return product, 201

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    ---- G -----
    Updates a product based on an id
    """
    product_data = request.get_json()
    try:
        result = ProductSchema(**product_data)
        updated_product_data = result.model_dump()
    except ValidationError as e:
        return e.json(), 400
    
    product = find_product_by_id(product_id)
    if product:
        product.update(updated_product_data)
        return product, 200
    
    return {"error": "Product not found"}, 404

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    ---- G -----
    Deletes a product based on a id
    """
    for index, product in enumerate(products.copy()):
        if product["id"] == product_id:
            products.pop(index)
            return {}, 204
    return {"error": "Product not found"}, 404


@app.route("/products/search", methods=["GET"])
def search_products():
    """
    ---- G -----
    Returns a list of all products which includes the search_query in the name
    """
    search_query = request.args.get("search_query")
    found_products = []
    for product in products:
        if search_query.lower() in product["name"].lower():
            found_products.append(product)
    return found_products, 200


@app.route("/products/stock_update/<int:product_id>", methods=["PUT"])
def product_stock_update(product_id):
    """
    --- VG ----
    This endpoint will update the stock for a specific product.
    The new stock quantity is passed as a query parameter.
    """
    quantity_update = request.args.get("quantity", type=int)

    if quantity_update is None or quantity_update < 0:
        return {"error": "A valid quantity parameter is required"}, 400

    product = find_product_by_id(product_id)
    if product:
        # Ensure the stock quantity does not go negative
        product["stock"] = quantity_update
        return product, 200

    return {"error": "Product not found"}, 404


@app.route("/products/bulk", methods=["POST"])
def create_product_bulk():
    """
    --- VG ----
    This endpoint receives a list of products and creates them.
    It uses a separate BulkCreateSchema, which only contains a list of products
    Example input:
    {
        "products": [
            {
                "name": "Work laptop4",
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
            ...
        ]
    }
    """
    try:
        bulk_data = request.get_json()
        result = BulkProductSchema(**bulk_data)
        result = result.model_dump()["products"]
    except ValidationError as e:
        return e.json(), 400

    added_products = []
    for product in result:
        product["id"] = get_next_id(products)
        products.append(product)
        added_products.append(product)

    return added_products, 201


@app.route("/products/bulk_update", methods=["PUT"])
def update_product_bulk():
    """
    --- VG ----
    This endpoint receives a list of products, looks at the id of each product 
    and tries to update it. If the id does not exist, it ignores it.
    
    Example input:
    [
    {
        "id": 1,
        "name": "Lenovo pro", 
        "price": 20.0, 
        "category": "Electronics", 
        "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
        "stock": 3
    },
    {
        "id": 2,
        "name": "Macbook pro", 
        "price": 20.0, 
        "category": "Electronics", 
        "specification": {"color": "white", "weight": 30.5, "height": 8.0, "length": 5.0},
        "stock": 2
    }
    ]
    """
    # updated_products_data = request.get_json()
    # updated_products = []
    # for product_data in updated_products_data:
    #     try:
    #         product_id = product_data.get("id")
    #         existing_product = find_product_by_id(product_id)

    #         if not existing_product:
    #             continue  # Skip if product not found

    #         result = ProductSchema(**product_data)
    #         updated_product_data = result.model_dump()
    #         existing_product.update(updated_product_data)
    #         updated_products.append(existing_product)

    #     except ValidationError as e:
    #         return e.json(), 400

    # return updated_products, 200 




    # try:
    #     updated_products_data = request.get_json()
    #     result = BulkProductSchema(**updated_products_data)
    #     updated_product_data = result.model_dump()["products"]
    # except ValidationError as e:
    #     return e.json(), 400    
    
    # updated_products = []
    # for product in updated_products_data["products"]:
    #     product_id = product.get("id")
    #     existing_product = find_product_by_id(product_id) 
    #     if not existing_product:
    #         continue  
    #     existing_product.update(product)
    #     updated_products.append(existing_product)

    # return updated_products, 200


    try:
        updated_products_data = request.get_json()
        BulkProductSchema(**updated_products_data)
    except ValidationError as e:
        return e.json(), 400    
    
    updated_products = []
    for product in updated_products_data["products"]:
        product_id = product["id"]
        existing_product = find_product_by_id(product_id) 
        if not existing_product:
            continue  
        existing_product.update(product)
        updated_products.append(existing_product)

    return updated_products, 200



    # try:
    #     updated_products_data = request.get_json()
    #     updated_product_data = []
    #     for product in updated_products_data:
    #         updated_product_data.append(ProductSchema(**product).model_dump())       
    # except ValidationError as e:
    #     return e.json(), 400

    # updated_products = []
    # for product in updated_product_data:
    #     product_id = product.get("id")
    #     existing_product = find_product_by_id(product_id) 
    #     if not existing_product:
    #         continue  
    #     existing_product.update(product)
    #     updated_products.append(existing_product)

    # return updated_products, 200





    # updated_products_data = request.get_json()
    # updated_products = []
    # for product_data in updated_products_data:
    #     try:
    #         product_id = product_data.get("id")
    #         existing_product = find_product_by_id(product_id)

    #         if not existing_product:
    #             continue  # Skip if product not found

    #         result = ProductSchema(**product_data)
    #         updated_product_data = result.model_dump()
    #         existing_product.update(updated_product_data)
    #         updated_products.append(existing_product)

    #     except ValidationError as e:
    #         return e.json(), 400

    # return updated_products, 200 



    # updated_products_data = request.get_json() 
    # updated_products = []
    # validation_errors = []

    # for product_data in updated_products_data:
    #     try:
    #         product_id = product_data.get("id")
    #         existing_product = find_product_by_id(product_id)

    #         if not existing_product:
    #             continue  

    #         result = ProductSchema(**product_data)
    #         updated_product_data = result.model_dump()
    #         existing_product.update(updated_product_data)
    #         updated_products.append(existing_product)

    #     except ValidationError as e:
    #         validation_errors.append(e)

    # if validation_errors:
    #     return {"errors": [error.json() for error in validation_errors]}, 400

    # return updated_products, 200


# # other simple solution
#     updated_products_data = request.get_json() 
#     updated_products = []
#     validation_errors = []

#     for product_data in updated_products_data:
#         try:
#             product_id = product_data.get("id")
#             existing_product = find_product_by_id(product_id)

#             if not existing_product:
#                 continue  

#             result = ProductSchema(**product_data)
#             updated_product_data = result.model_dump()
#             existing_product.update(updated_product_data)
#             updated_products.append(existing_product)

#         except ValidationError as e:
#             validation_errors.append(e.json())

#     if validation_errors:
#         return validation_errors, 400

#     return updated_products, 200