from flask import Flask, render_template, url_for, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from Product import Product
import Repository
from datetime import datetime
import json
from callGpt import GPTModelClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product3.db'
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
    
    retrieved_product1 = Repository.getProduct(product_id1)
    retrieved_product2 = Repository.getProduct(product_id2)
    result = []
    print("product1_features  ",retrieved_product1.features.replace("'", "\""))

    product1_features=json.loads(retrieved_product1.features.replace("'", "\""))

    product2_features=json.loads(retrieved_product2.features.replace("'", "\""))

    if retrieved_product1.features and retrieved_product2.features:
       common_features= set(product1_features) & set(product2_features)
    if retrieved_product1:
        print("retrieved_product1  ", retrieved_product1)
        product1 = Product(id=retrieved_product1.productId, name=retrieved_product1.name, features={key: product1_features[key] for key in common_features}, price=retrieved_product1.price)
        result.append(product1)
    if retrieved_product2:
        print("retrieved_product2  ", retrieved_product2)
        product2 = Product(id=retrieved_product2.productId, name=retrieved_product2.name, features={key: product2_features[key] for key in common_features}, price=retrieved_product2.price)
        result.append(product2)
    return json.dumps([res.__dict__ for res in result])

@app.route('/getFeatureDetails', methods=['GET'])
def get_feature():
    res = {}
    featureKey = request.args.get('feature')
    feature_prod1 = request.args.get('featureProd1')
    feature_prod2 = request.args.get('featureProd2')
    prodId1 = request.args.get('prodId1')
    prodId2 = request.args.get('prodId1')
    print("feature ",featureKey)
    print("prodId2 ",prodId2)
    print("prodId1 ",prodId1)
    retrieved_product1 = Repository.getProduct(prodId1)
    retrieved_product2 = Repository.getProduct(prodId2)
    if retrieved_product1.productType != retrieved_product2.productType :
        return jsonify({'error': 'Both product should be of similar type'}), 400
    gpt = GPTModelClient()
    print("retrieved_product1.productType  ",retrieved_product1.productType)
    user_input = "{} {} vs {} explain this in context of {} to non tech person as short as possible. Please stick to context. Also please don't echo back the user input without adding any accompanying text".format(featureKey, feature_prod1, feature_prod2, retrieved_product1.productType)
    res = {featureKey : gpt.query_gpt(user_input)}
    return json.dumps(res)

if __name__ == '__main__':
    app.run(debug=True)
