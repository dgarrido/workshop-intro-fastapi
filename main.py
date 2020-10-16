from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import models, schema


app = FastAPI()

engine = create_engine('sqlite:///ifa.sqlite')

models.init_db(engine)
"""
Session = sessionmaker(bind=engine, autocommit=True, autoflush=True)
session = Session()
"""
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


@app.get("/products")
def get_all_products():
    """
        Retrieve all products
    """
    products = db_session.query(models.Product).all()
    return products

@app.get("/product/{product_id}")
def get_product(product_id: int):
    product = db_session.query(models.Product).get(product_id)
    return product
    
@app.post("/product")
def insert_product(product: schema.Product):
    """
        Insert a product on DB
    """
    db_session.add(
        models.Product(
            **dict(product)
        )
    )
    db_session.commit()

    return {
        "msg": "Product created successfully!",
        "product": product
    }

@app.put("/product/{product_id}")
def update_product(product_id: int, product: schema.Product):
    """
        Updates a product on DB
    """
    product = dict(product)
    product['id'] = product_id
    db_session.merge(models.Product(**product))
    db_session.commit()

    return {
        "msg": "Product updated successfully!",
        "product": product,
        "product_id": product_id
    }

@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    product = db_session.query(models.Product).get(product_id)
    db_session.delete(product)
    db_session.commit()

    return {
        "msg": "Product deleted successfully!",
        "product_id": product_id
    }

@app.get("/cart/{cart_id}")
def get_cart(cart_id: int):
    cart = db_session.query(models.Cart).get(cart_id)
    return cart

@app.post("/cart")
def insert_cart(cart: schema.Cart):
    """
        Create a new cart
    """
    cart_obj = models.Cart()

    for line in cart.cart_order_lines:
        cart_obj.lines.append(
            models.CartLine(
                cart=cart_obj,
                product_id=line.product_id,
                quantity=line.quantity
            )
        )

    db_session.add(cart_obj)
    db_session.commit()

    carts = db_session.query(models.Cart).all()

    return {
        "msg": "Cart created successfully!",
        "carts": carts,
    }

@app.put("/cart/{cart_id}")
def update_cart(cart_id: int, cart: schema.Cart):
    """
        Updates a cart
    """
    cart_obj = db_session.query(models.Cart).get(cart_id)

    cart_obj.lines = []

    for line in cart.cart_order_lines:
        cart_obj.lines.append(
            models.CartLine(
                cart=cart_obj,
                product_id=line.product_id,
                quantity=line.quantity
            )
        )

    db_session.add(cart_obj)
    db_session.commit()

    carts = db_session.query(models.Cart).all()

    return {
        "msg": "Cart updated successfully!",
        "carts": carts,
    }

@app.delete("/cart/{cart_id}")
def delete_cart(cart_id: int):
    cart = db_session.query(models.Cart).get(cart_id)
    db_session.delete(cart)
    db_session.commit()

    return {
        "msg": "Cart deleted successfully!",
        "cart_id": cart_id
    }