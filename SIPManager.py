import streamlit as st
import pandas as pd

# Function to calculate SIP amounts
def calculate_sip(goal_value, tenure, step_up_rate=0):
    monthly_tenure = tenure * 12
    if step_up_rate == 0:
        # No Step-up SIP
        sip_amount = goal_value / monthly_tenure
        return sip_amount
    else:
        # Step-up SIP
        sip_amount = goal_value / (monthly_tenure * (1 + step_up_rate / 100))
        return sip_amount

# Function to suggest mutual funds based on risk appetite
def suggest_mutual_funds(risk_appetite):
    funds = {
        "Aggressive": [
            {"Fund Name": "Fund A", "Rating": 4.5},
            {"Fund Name": "Fund B", "Rating": 4.3},
            {"Fund Name": "Fund C", "Rating": 4.2},
        ],
        "Moderate": [
            {"Fund Name": "Fund D", "Rating": 4.4},
            {"Fund Name": "Fund E", "Rating": 4.1},
            {"Fund Name": "Fund F", "Rating": 4.0},
        ],
        "Conservative": [
            {"Fund Name": "Fund G", "Rating": 4.6},
            {"Fund Name": "Fund H", "Rating": 4.3},
            {"Fund Name": "Fund I", "Rating": 4.2},
        ],
    }
    return funds.get(risk_appetite, [])

# Streamlit app
st.title("Mutual Fund SIP Planner")

# User inputs
goal_value = st.number_input("Enter your Goal Value (₹):", min_value=0, step=1000)
tenure = st.number_input("Enter your Goal Tenure (in years):", min_value=1, step=1)
risk_appetite = st.selectbox(
    "Select your Risk Appetite:", ["Aggressive", "Moderate", "Conservative"]
)

if st.button("Suggest Funds"):
    if goal_value > 0 and tenure > 0:
        # Suggest mutual funds
        funds = suggest_mutual_funds(risk_appetite)
        st.subheader("Suggested Mutual Funds:")
        st.table(pd.DataFrame(funds))

        # Calculate SIP amounts
        no_stepup_sip = calculate_sip(goal_value, tenure)
        stepup_sip = calculate_sip(goal_value, tenure, step_up_rate=10)

        st.subheader("SIP Amounts:")
        st.write(f"No Step-up SIP: ₹{no_stepup_sip:.2f} per month")
        st.write(f"Step-up SIP (10% annual increase): ₹{stepup_sip:.2f} per month")
    else:
        st.error("Please enter valid Goal Value and Tenure.")
