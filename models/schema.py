from pydantic import BaseModel, conint, constr
from typing import List, Optional


class Product(BaseModel):
    name: constr(max_length=50)
    price: float
    category: str
    description: Optional[str]
    image_path: Optional[str]



class CartOrderLine(BaseModel):
    product_id: int
    quantity: conint(ge=1)


class Cart(BaseModel):
    cart_order_lines: List[CartOrderLine]


class BillingAddress(BaseModel):
    first_name: str
    last_name: str
    vat: str
    email: str
    address: Optional[str]


class Order(Cart):
    code: str
    billing_address: BillingAddress