import streamlit as st
from prediction_helper import predict
import matplotlib.pyplot as plt
import numpy as np

# Set the page configuration and title
st.set_page_config(
    page_title="Credit Risk Modelling",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 0.3rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #E6F3FF;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        width: 100%;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2D4BA9;
        color: white;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #6B7280;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Credit Risk Modelling</h1>', unsafe_allow_html=True)

# Introduction
st.markdown("""
This tool helps assess credit risk by calculating default probability, credit score, and rating based on applicant information.
Please fill in the details below and click 'Calculate Risk' to get the results.
""")

# Create two main columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="sub-header">Applicant Information</div>', unsafe_allow_html=True)

    # Create rows for input fields
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)

    # Assign inputs to the first row with default values
    with row1[0]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28, help="Applicant's age in years")
        st.markdown('</div>', unsafe_allow_html=True)
    with row1[1]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        income = st.number_input('Annual Income (₹)', min_value=0, value=1200000,
                                 help="Applicant's annual income in Indian Rupees")
        st.markdown('</div>', unsafe_allow_html=True)
    with row1[2]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000,
                                      help="Requested loan amount in Indian Rupees")
        st.markdown('</div>', unsafe_allow_html=True)

    # Calculate Loan to Income Ratio and display it
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    with row2[0]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Loan to Income Ratio", f"{loan_to_income_ratio:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Assign inputs to the remaining controls
    with row2[1]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36,
                                             help="Duration of the loan in months")
        st.markdown('</div>', unsafe_allow_html=True)
    with row2[2]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_dpd_per_delinquency = st.number_input('Average Days Past Due (DPD)', min_value=0, value=20,
                                                  help="Average days past due per delinquency event")
        st.markdown('</div>', unsafe_allow_html=True)

    with row3[0]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30,
                                            help="Percentage of delinquent accounts")
        st.markdown('</div>', unsafe_allow_html=True)
    with row3[1]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100, step=1,
                                                   value=30, help="Percentage of available credit being used")
        st.markdown('</div>', unsafe_allow_html=True)
    with row3[2]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2,
                                            help="Number of currently open loan accounts")
        st.markdown('</div>', unsafe_allow_html=True)

    with row4[0]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'],
                                      help="Applicant's current residence type")
        st.markdown('</div>', unsafe_allow_html=True)
    with row4[1]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'],
                                    help="Purpose of the loan")
        st.markdown('</div>', unsafe_allow_html=True)
    with row4[2]:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'], help="Type of loan being applied for")
        st.markdown('</div>', unsafe_allow_html=True)

    # Button to calculate risk
    if st.button('Calculate Risk'):
        with st.spinner('Calculating risk assessment...'):
            probability, credit_score, rating = predict(age, income, loan_amount, loan_tenure_months,
                                                        avg_dpd_per_delinquency,
                                                        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                                                        residence_type, loan_purpose, loan_type)

with col2:
    st.markdown('<div class="sub-header">Risk Assessment Results</div>', unsafe_allow_html=True)

    if 'probability' in locals():
        # Display the results in a visually appealing way
        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        # Determine color based on probability
        if probability < 0.3:
            color = "green"
        elif probability < 0.6:
            color = "orange"
        else:
            color = "red"

        st.markdown(f"<h3 style='text-align: center; color: {color};'>Default Probability: {probability:.2%}</h3>",
                    unsafe_allow_html=True)

        # Credit score with color coding
        if credit_score >= 750:
            score_color = "green"
        elif credit_score >= 650:
            score_color = "orange"
        else:
            score_color = "red"

        st.markdown(f"<h3 style='text-align: center; color: {score_color};'>Credit Score: {credit_score}</h3>",
                    unsafe_allow_html=True)

        # Rating with color coding
        rating_colors = {
            'Poor': 'red',
            'Average': 'orange',
            'Good': 'blue',
            'Excellent': 'green'
        }
        st.markdown(
            f"<h3 style='text-align: center; color: {rating_colors.get(rating, 'black')};'>Rating: {rating}</h3>",
            unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Add a simple visualization
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.barh([0], [probability], color=color, alpha=0.7)
        ax.set_xlim(0, 1)
        ax.set_xlabel('Default Probability')
        ax.set_title('Risk Level')
        ax.set_yticks([])
        st.pyplot(fig)

        # Recommendation based on rating
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("**Recommendation:**")
        if rating == 'Excellent':
            st.success("Low risk: Recommended for approval with favorable terms.")
        elif rating == 'Good':
            st.info("Moderate risk: Recommended for approval with standard terms.")
        elif rating == 'Average':
            st.warning("Elevated risk: Consider with higher interest rates or additional collateral.")
        else:
            st.error("High risk: Not recommended for approval.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Please fill in the applicant information and click 'Calculate Risk' to see results here.")

# Footer
st.markdown('<div class="footer">Project From Codebasics ML Course</div>', unsafe_allow_html=True)