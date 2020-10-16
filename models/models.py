from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Model = declarative_base(name='Model')

def init_db(engine):
    Model.metadata.create_all(bind=engine)

class Product(Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_path = Column(String, nullable=True)

    cart_lines = relationship("CartLine", back_populates="product")


class Cart(Model):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    lines = relationship("CartLine", back_populates="cart", cascade="all, delete-orphan", lazy="joined")


class CartLine(Model):
    __tablename__ = 'cart_lines'
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("cart.id")) #, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id")) #, primary_key=True)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart",foreign_keys=[cart_id])
    product = relationship("Product", foreign_keys=[product_id])