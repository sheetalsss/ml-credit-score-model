import joblib
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Path to the saved model and its components
MODEL_PATH = 'artifacts/model_data.joblib'


def load_model_data():
    """Load model data with proper error handling"""
    try:
        # Check if file exists
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

        # Try to load the model
        model_data = joblib.load(MODEL_PATH)

        # Validate the loaded data
        required_keys = ['model', 'scaler', 'features', 'cols_to_scale']
        for key in required_keys:
            if key not in model_data:
                raise ValueError(f"Missing key in model data: {key}")

        return model_data

    except Exception as e:
        raise Exception(f"Error loading model: {str(e)}")


# Load the model data
try:
    model_data = load_model_data()
    model = model_data['model']
    scaler = model_data['scaler']
    features = model_data['features']
    cols_to_scale = model_data['cols_to_scale']
except Exception as e:
    # This will help debug in Streamlit
    print(f"Model loading failed: {e}")
    model = None
    scaler = None
    features = None
    cols_to_scale = None


def prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                  delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                  loan_purpose, loan_type):
    if model is None:
        raise ValueError("Model not loaded. Cannot prepare input.")

    # Create a dictionary with input values
    input_data = {
        'age': age,
        'loan_tenure_months': loan_tenure_months,
        'number_of_open_accounts': num_open_accounts,
        'credit_utilization_ratio': credit_utilization_ratio,
        'loan_to_income': loan_amount / income if income > 0 else 0,
        'delinquency_ratio': delinquency_ratio,
        'avg_dpd_per_delinquency': avg_dpd_per_delinquency,
        'residence_type_Owned': 1 if residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residence_type == 'Rented' else 0,
        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,
        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0,
        # Dummy values for missing features
        'number_of_dependants': 1,
        'years_at_current_address': 1,
        'zipcode': 1,
        'sanction_amount': 1,
        'processing_fee': 1,
        'gst': 1,
        'net_disbursement': 1,
        'principal_outstanding': 1,
        'bank_balance_at_application': 1,
        'number_of_closed_accounts': 1,
        'enquiry_count': 1
    }

    df = pd.DataFrame([input_data])
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df = df[features]

    return df


def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    if model is None:
        return 0.5, 600, "Error: Model not loaded"

    try:
        input_df = prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                                 delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                                 loan_purpose, loan_type)

        probability, credit_score, rating = calculate_credit_score(input_df)
        return probability, credit_score, rating

    except Exception as e:
        return 0.5, 600, f"Error: {str(e)}"


def calculate_credit_score(input_df, base_score=300, scale_length=600):
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_
    default_probability = 1 / (1 + np.exp(-x))
    non_default_probability = 1 - default_probability
    credit_score = base_score + non_default_probability.flatten() * scale_length

    def get_rating(score):
        if 300 <= score < 500:
            return 'Poor'
        elif 500 <= score < 650:
            return 'Average'
        elif 650 <= score < 750:
            return 'Good'
        elif 750 <= score <= 900:
            return 'Excellent'
        else:
            return 'Undefined'

    rating = get_rating(credit_score[0])
    return default_probability.flatten()[0], int(credit_score[0]), rating