from flask import Flask, render_template, url_for, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from Product import Product
import Repository
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)

@app.route('/getProduct', methods=['GET'])
def get_product():
    # Get the parameters from the request
    product_id1 = request.args.get('product_id1')
    product_id2 = request.args.get('product_id2')
    print("product_id1  ",product_id1)
    print(type(product_id1))

    # Check if both parameters are provided
    if product_id1 is None or product_id2 is None:
        return jsonify({'error': 'Both product_id and product_name are required'}), 400
    
    retrieved_product = Repository.getProduct(product_id1)

    if retrieved_product:
        print("retrieved_product  ", retrieved_product)
        product = Product(id=retrieved_product.productId, name=retrieved_product.name, features=json.loads(retrieved_product.features), price=retrieved_product.price)
        print("product retived  ",product)
        print("product json  ",jsonify(product.__dict__))
        return jsonify(product.__dict__)

if __name__ == '__main__':
    app.run(debug=True)
