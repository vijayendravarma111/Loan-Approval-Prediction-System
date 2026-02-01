import streamlit as st
import pandas as pd
import pickle

# Load trained model
model = pickle.load(open('loan_model.pkl', 'rb'))

st.set_page_config(page_title="Loan Approval Predictor", layout="wide")

st.title("🏦 Loan Approval Prediction System")
st.markdown("### Enter applicant details and get instant decision")

# Create two columns
col1, col2 = st.columns([2, 1])

# ================= LEFT COLUMN – INPUTS =================
with col1:
    st.subheader("📋 Applicant Details")

    no_of_dependents = st.number_input("Number of Dependents", 0, 10, 0)
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["No", "Yes"])

    income_annum = st.number_input("Annual Income (₹)", min_value=0, step=50000)
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0, step=50000)
    loan_term = st.number_input("Loan Term (Years)", 1, 30)

    cibil_score = st.number_input("CIBIL Score", 300, 900, 700)

    res_assets = st.number_input("Residential Assets Value (₹)", min_value=0, step=50000)
    com_assets = st.number_input("Commercial Assets Value (₹)", min_value=0, step=50000)
    lux_assets = st.number_input("Luxury Assets Value (₹)", min_value=0, step=50000)
    bank_assets = st.number_input("Bank Asset Value (₹)", min_value=0, step=50000)

    check_btn = st.button("🔍 Check Loan Status")

# ================= RIGHT COLUMN – OUTPUT =================
with col2:
    st.subheader("📊 Loan Decision")

    if check_btn:
        # Encode inputs
        education_enc = 1 if education == "Graduate" else 0
        self_employed_enc = 1 if self_employed == "Yes" else 0

        sample = pd.DataFrame({
            'no_of_dependents': [no_of_dependents],
            'education': [education_enc],
            'self_employed': [self_employed_enc],
            'income_annum': [income_annum],
            'loan_amount': [loan_amount],
            'loan_term': [loan_term],
            'cibil_score': [cibil_score],
            'residential_assets_value': [res_assets],
            'commercial_assets_value': [com_assets],
            'luxury_assets_value': [lux_assets],
            'bank_asset_value': [bank_assets]
        })

        prediction = model.predict(sample)[0]

        st.markdown("---")

        if prediction == 1:
            st.success("### ✅ Loan Approved")
            st.balloons()
        else:
            st.error("### ❌ Loan Rejected")
    else:
        st.info("👈 Fill the form and click **Check Loan Status**")
