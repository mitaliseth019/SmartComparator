from flask_sqlalchemy import SQLAlchemy
import json
from flask import Flask
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)

class ProductDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    features = db.Column(db.Text)
    price = db.Column(db.Float)

db.create_all()

# Add data to the ProductDB database
def add_or_update_product(productId, name, description, features, price):
    product = ProductDB.query.filter_by(productId=productId).first()
    if product:
        # Update the existing product
        product.name = name
        product.description = description
        product.features = features
        product.price = price
    else:
        # Add a new product
        product = ProductDB(productId=productId, name=name, description=description, features=features, price=price)
        db.session.add(product)
    db.session.commit()

# Example data
# features_list1 = {"Operating_System": "iOS", "Display_Size": "6.1-inch Super Retina XDR display", 
#      "Processor": "A14 Bionic chip", "Camera": "Dual-camera system", 
#      "Security": "Face ID", "Design": "Ceramic Shield front cover", 
#      "Durability": "Water and dust resistant (IP68)", "Connectivity": "5G capable", 
#      "Charging": "Wireless charging", "Color_Options": "Available in multiple colors"}
# features_json1 = json.dumps(features_list1)

# features_list2 = {"Operating_System": "Android", "Display_Size": "6.2-inch Quad HD+ Dynamic AMOLED display", 
#      "Processor": "Snapdragon 865 processor", "Camera": "Triple-camera system", 
#      "Security": "Ultrasonic fingerprint sensor", "Connectivity": "5G capable", 
#      "Special_Features": "Wireless PowerShare", 
#      "Durability": "IP68 water and dust resistance", 
#      "Charging": "Fast charging", "Storage_Options": "Expandable storage"}
# features_json2 = json.dumps(features_list2)
# product_data = [
#     {"productId": "prod123", "name": "iPhone 12", "description": "Apple smartphone", "features": features_json1, "price": 100},
#     {"productId": "prod234","name": "Samsung Galaxy S20", "description": "Android smartphone", "features": features_json2, "price": 150}
# ]

product_df=pd.read_csv('products1.csv')
# Add example data to the database
for data in product_df:
    add_or_update_product(data['ProductId'], data['Product_Name'], data['Desc'], data['selected_features'], data['Price'],data['Review'])  

print("productId  ",ProductDB.query.filter_by(productId="prod123").first())

def getProduct(id):
    return ProductDB.query.filter_by(productId=id).first()