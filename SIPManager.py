import streamlit as st
import pandas as pd

# Function to calculate future value of the goal
def calculate_future_value(goal_value, tenure, inflation_rate=6):
    """
    Calculate the future value of the goal amount considering inflation.
    """
    future_value = goal_value * ((1 + inflation_rate / 100) ** tenure)
    return future_value

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

# Placeholder function to fetch mutual funds with 4+ star ratings
def fetch_mutual_funds(risk_appetite):
    """
    Fetch mutual funds with 4+ star ratings based on risk appetite.
    Replace this with actual API calls or web scraping logic.
    """
    # Simulated mutual funds data
    funds = {
        "Aggressive": [
            {"Fund Name": "Axis Growth Opportunities Fund", "Rating": 4.5},
            {"Fund Name": "Mirae Asset Emerging Bluechip Fund", "Rating": 4.3},
            {"Fund Name": "SBI Small Cap Fund", "Rating": 4.2},
        ],
        "Moderate": [
            {"Fund Name": "HDFC Balanced Advantage Fund", "Rating": 4.4},
            {"Fund Name": "ICICI Prudential Equity & Debt Fund", "Rating": 4.1},
            {"Fund Name": "Kotak Standard Multicap Fund", "Rating": 4.0},
        ],
        "Conservative": [
            {"Fund Name": "ICICI Prudential Regular Savings Fund", "Rating": 4.6},
            {"Fund Name": "HDFC Short Term Debt Fund", "Rating": 4.3},
            {"Fund Name": "Axis Treasury Advantage Fund", "Rating": 4.2},
        ],
    }
    return funds.get(risk_appetite, [])

# Streamlit app
st.title("Mutual Fund SIP Planner")

# User inputs
goal_value = st.number_input("Enter your Current Goal Value (₹):", min_value=0, step=1000)
tenure = st.number_input("Enter your Goal Tenure (in years):", min_value=1, step=1)
risk_appetite = st.selectbox(
    "Select your Risk Appetite:", ["Aggressive", "Moderate", "Conservative"]
)

if st.button("Calculate and Suggest Funds"):
    if goal_value > 0 and tenure > 0:
        # Calculate future value of the goal
        future_value = calculate_future_value(goal_value, tenure)
        st.subheader("Future Value of Your Goal:")
        st.write(f"₹{future_value:,.2f} (considering 6% annual inflation)")

        # Suggest mutual funds
        funds = fetch_mutual_funds(risk_appetite)
        st.subheader("Suggested Mutual Funds:")
        st.table(pd.DataFrame(funds))

        # Calculate SIP amounts
        no_stepup_sip = calculate_sip(future_value, tenure)
        stepup_sip = calculate_sip(future_value, tenure, step_up_rate=10)

        st.subheader("SIP Amounts:")
        st.write(f"No Step-up SIP: ₹{no_stepup_sip:.2f} per month")
        st.write(f"Step-up SIP (10% annual increase): ₹{stepup_sip:.2f} per month")
    else:
        st.error("Please enter valid Goal Value and Tenure.")
