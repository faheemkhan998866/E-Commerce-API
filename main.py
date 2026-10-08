from fastapi import FastAPI
from bson import ObjectId
from database import db
from models import Product
from routes.users import router as users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router)


@app.get("/")
def home():
    return {"Message": "E-Commerce API is running"}



@app.post("/products")
def create_product(product: Product):
    result = db["products"].insert_one(product.model_dump())

    return {
        "message": "Product created successfully",
        "product_id": str(result.inserted_id)
    }


@app.get("/products")
def get_products():
    products = list(db["products"].find())

    for product in products:
        product["_id"] = str(product["_id"])

    return products


@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = db["products"].find_one({
        "_id": ObjectId(product_id)
    })

    if product:
        product["_id"] = str(product["_id"])
        return product

    return {
        "message": "Product not found"
    }



@app.put("/products/{product_id}")
def update_product(product_id: str, product: Product):

    result = db["products"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.model_dump()}
    )

    if result.matched_count == 0:
        return {
            "message": "Product not found"
        }

    return {
        "message": "Product updated successfully"
    }




@app.delete("/products/{product_id}")
def delete_product(product_id: str):

    result = db["products"].delete_one({
        "_id": ObjectId(product_id)
    })

    if result.deleted_count == 0:
        return {
            "message": "Product not found"
        }

    return {
        "message": "Product deleted successfully"
    }



@app.get("/products/category/{category}")
def get_products_by_category(category: str):

    products = list(db["products"].find({
        "category": category
    }))

    for product in products:
        product["_id"] = str(product["_id"])

    return products