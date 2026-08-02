# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
Product_Store_Sales_Total_predictor_api = Flask("Super Kart Total Sales Prediction")

# Load the trained machine learning model
model = joblib.load("super_kart_product_store_sales_prediction_model_v1_0.joblib")


# Define a route for the home page (GET request)
@Product_Store_Sales_Total_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Total Sales Prediction API!"


# Define an endpoint for single product-store prediction (POST request)
@Product_Store_Sales_Total_predictor_api.post('/v1/totalsales')
def predict_Sales_Total():
    """
    This function handles POST requests to the '/v1/totalsales' endpoint.
    It expects a JSON payload containing product/store details and returns
    the predicted total sales as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    # NOTE: Replace these keys with the exact feature names/order used to train your model
    sample = {
        'Product_Weight': property_data['Product_Weight'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'], 
        'Product_MRP': property_data['Product_MRP'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type'],
        'Product_Id_char': property_data['Product_Id_char'],
        'Store_Age_Years': property_data['Store_Age_Years'],
        'Product_Type_Category': property_data['Product_Type_Category']

    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    predict_product_total_sales = model.predict(input_data)[0]

    # Convert prediction to Python float
    # This conversion is needed because model.predict() can return a NumPy float32,
    # and jsonify() can't serialize that directly.
    predicted_total_sale = round(float(predict_product_total_sales), 2)

    # Return the total sales
    return jsonify({'Predicted Total Sales (in dollars)': predicted_total_sale})


# Define an endpoint for batch prediction (POST request)
@Product_Store_Sales_Total_predictor_api.post('/v1/totalsalebatch')
def predict_Sales_Total_batch():
    """
    This function handles POST requests to the '/v1/totalsalebatch' endpoint.
    It expects a CSV file containing product/store details for multiple
    product-store combinations and returns the predicted total sales as a
    dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all rows in the DataFrame
    predicted_sales_raw = model.predict(input_data).tolist()

    # Convert to plain Python floats, rounded
    predicted_sales = [round(float(sale), 2) for sale in predicted_sales_raw]

    # Create a dictionary of predictions with Product_Store IDs as keys
    product_store_ids = input_data['Product_Store_Id'].tolist()
    output_dict = dict(zip(product_store_ids, predicted_sales))

    return jsonify(output_dict)


# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    Product_Store_Sales_Total_predictor_api.run(debug=True)
