import streamlit as st
import pickle
import pandas as pd

# Load model and columns
model = pickle.load(open('model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))

st.title("🏠 Delhi House Price Prediction")

# ---------------- INPUTS ---------------- #
st.sidebar.header("Enter House Details")

area = st.sidebar.number_input("Area (sq ft)", min_value=100, max_value=10000)
bhk = st.sidebar.number_input("BHK", min_value=1, max_value=10)
bathroom = st.sidebar.number_input("Bathrooms", min_value=1, max_value=10)

# These must match your dataset categories
localities = [col.replace("Locality_", "") for col in columns if "Locality_" in col]
furnishing_types = [col.replace("Furnishing_", "") for col in columns if "Furnishing_" in col]

location = st.sidebar.selectbox("Location", sorted(localities))
furnishing = st.sidebar.selectbox("Furnishing", sorted(furnishing_types))

# ---------------- PREDICTION ---------------- #
if st.button("Predict Price"):

    # Create empty dataframe with all columns
    input_data = pd.DataFrame([0]*len(columns)).T
    input_data.columns = columns

    # Fill numeric values
    if 'Area' in input_data.columns:
        input_data.at[0, 'Area'] = area
    if 'BHK' in input_data.columns:
        input_data.at[0, 'BHK'] = bhk
    if 'Bathroom' in input_data.columns:
        input_data.at[0, 'Bathroom'] = bathroom

    # Set locality
    loc_col = f"Locality_{location}"
    if loc_col in input_data.columns:
        input_data.at[0, loc_col] = 1

    # Set furnishing
    furn_col = f"Furnishing_{furnishing}"
    if furn_col in input_data.columns:
        input_data.at[0, furn_col] = 1

    # Prediction
    prediction = model.predict(input_data)

    st.success(f"Estimated Price: ₹ {prediction[0]:,.2f}")