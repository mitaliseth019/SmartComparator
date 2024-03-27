from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    features = db.Column(db.Text)
    price = db.Column(db.Float)

db.create_all()

# Add data to the Product database
def add_product(name, description, features, price):
    product = Product(name=name, description=description, features=features, price=price)
    db.session.add(product)
    db.session.commit()

# Example data
features_list1 = ["iOS", "6.1-inch Super Retina XDR display", "A14 Bionic chip", "Dual-camera system", "Face ID", "Ceramic Shield front cover", "Water and dust resistant (IP68)", "5G capable", "Wireless charging", "Available in multiple colors"]
features_json1 = json.dumps(features_list1)

features_list2 = ["Android", "6.2-inch Quad HD+ Dynamic AMOLED display", "Snapdragon 865 processor", "Triple-camera system", "Ultrasonic fingerprint sensor", "Wireless PowerShare", "IP68 water and dust resistance", "5G capable", "Fast charging", "Expandable storage"]
features_json2 = json.dumps(features_list2)
product_data = [
    {"name": "iPhone 12", "description": "Apple smartphone", "features": features_json1, "price": 100},
    {"name": "Samsung Galaxy S20", "description": "Android smartphone", "features": features_json2, "price": 150},
    # Add more product data here
]

# Add example data to the database
for data in product_data:
    add_product(data['name'], data['description'], data['features'], data['price'])    

# Deserialize the string back to a list when retrieving it from the database
retrieved_product = Product.query.filter_by(name='iPhone 12').first()
print("retrieved_product  ", retrieved_product)
retrieved_features_json = retrieved_product.features
retrieved_features_list = json.loads(retrieved_features_json)
print("retrieved_features_list  ",retrieved_features_list)

# @app.route('/')
# def index():
#     # Example user query
#     user_query = "best smartphone under $500"
    
#     # Recommend top products based on user query
#     top_products = recommend_products(user_query)
    
#     # Instantiate GPTModelClient
#     gpt_client = GPTModelClient()
    
#     # Query GPT for response
#     gpt_response = gpt_client.query_gpt(user_query)
    
#     # Render HTML template with top recommended products and GPT response
#     return render_template('index.html', top_products=top_products, gpt_response=gpt_response)

if __name__ == '__main__':
    app.run(debug=True)
