import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Product Total Sale Prediction")

# ----------------------------------------------------------------------
# Section for online (single-record) prediction
# ----------------------------------------------------------------------
st.subheader("Online Prediction")

# --- Product ID -> derive category from the first two letters ---
Product_Id_input = st.text_input("Product ID").upper()

if Product_Id_input.startswith("FD"):
    Product_Id_char = "FD"
elif Product_Id_input.startswith("NC"):
    Product_Id_char = "NC"
elif Product_Id_input.startswith("DR"):
    Product_Id_char = "DR"
else:
    Product_Id_char = None
    st.warning("Product ID must start with 'FD', 'NC', or 'DR'.")

# --- Remaining feature inputs ---
Product_Weight = st.number_input("Product Weight", min_value=4.0, max_value=22.0, step=1.0)
Product_Sugar_Content = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar", "reg"])
Product_Allocated_Area = st.number_input("Allocated Area Ratio", min_value=0.004, max_value=0.298, step=0.001, value=0.05)
Product_Type = st.selectbox("Product Type", ["Perishable", "Non-Perishable"])
Product_MRP = st.number_input("Product MRP", min_value=30.0, max_value=270.0, step=0.5)
Store_Age_Years = st.number_input("Store Age", min_value=15, max_value=40, step=1)
Store_Size = st.selectbox("Store Size", ["Medium", "High", "Small"])
Store_Location_City_Type = st.selectbox("Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])

# Convert user input into a single-row DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Product_Id_char': Product_Id_char,
    'Store_Age_Years': Store_Age_Years,
    'Product_Type_Category': Product_Type
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    if Product_Id_char is None:
        st.error("Please enter a valid Product ID before predicting.")
    else:
        response = requests.post(f"{BACKEND_URL}/v1/totalsales", json=input_data.to_dict(orient='records')[0])
        if response.status_code == 200:
            prediction = response.json()['Predicted_Total_Sales']
            st.success(f"Predicted Product Total Sales: {prediction}")
        else:
            st.error("Unable to connect to the prediction API.")

# ----------------------------------------------------------------------
# Section for batch prediction
# ----------------------------------------------------------------------
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/totalsalebatch", files={"file": uploaded_file})
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)
        else:
            st.error("Unable to connect to the prediction API.")
