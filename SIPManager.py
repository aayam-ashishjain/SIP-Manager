import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to calculate future value of the goal
def calculate_future_value(goal_value, tenure, inflation_rate):
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

# Function to fetch mutual funds dynamically from Morningstar
def fetch_mutual_funds(risk_appetite):
    """
    Fetch mutual funds with 4+ star ratings dynamically from Morningstar.
    """
    url = "https://www.morningstar.com/funds/xray"  # Example URL (adjust based on Morningstar's structure)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Parse the mutual fund data (this is an example; adjust based on Morningstar's HTML structure)
    funds = []
    for fund in soup.find_all("div", class_="fund-row"):  # Adjust class name as per Morningstar's structure
        name = fund.find("a", class_="fund-name").text.strip()
        rating = float(fund.find("span", class_="star-rating").text.strip())
        expense_ratio = float(fund.find("span", class_="expense-ratio").text.strip().replace("%", ""))
        if rating >= 4:  # Only include funds with 4+ star ratings
            funds.append({"Fund Name": name, "Rating": rating, "Expense Ratio": expense_ratio})
    
    # Filter funds based on risk appetite (example logic)
    if risk_appetite == "Aggressive":
        funds = funds[:3]  # Top 3 funds for aggressive investors
    elif risk_appetite == "Moderate":
        funds = funds[3:6]  # Next 3 funds for moderate investors
    elif risk_appetite == "Conservative":
        funds = funds[6:9]  # Next 3 funds for conservative investors

    return funds

# Streamlit app
st.title("Mutual Fund SIP Planner")

# User inputs
goal_value = st.number_input("Enter your Current Goal Value (₹):", min_value=0, step=1000)
tenure = st.number_input("Enter your Goal Tenure (in years):", min_value=1, step=1)
inflation_rate = st.number_input("Enter the Rate of Inflation (%):", min_value=0.0, step=0.1)
risk_appetite = st.selectbox(
    "Select your Risk Appetite:", ["Aggressive", "Moderate", "Conservative"]
)

if st.button("Calculate and Suggest Funds"):
    if goal_value > 0 and tenure > 0:
        # Calculate future value of the goal
        future_value = calculate_future_value(goal_value, tenure, inflation_rate)
        st.subheader("Future Value of Your Goal:")
        st.write(f"₹{future_value:,.2f} (considering {inflation_rate}% annual inflation)")

        # Fetch mutual funds dynamically
        funds = fetch_mutual_funds(risk_appetite)
        if funds:
            st.subheader("Suggested Mutual Funds:")
            for fund in funds:
                st.write(f"Fund Name: {fund['Fund Name']}")
                st.write(f"Rating: {fund['Rating']} stars")
                st.write(f"Expense Ratio: {fund['Expense Ratio']}%")
                # Calculate investment allocation
                allocation = future_value / len(funds)
                st.write(f"Suggested Investment: ₹{allocation:,.2f}")
                st.write("---")
        else:
            st.error("No funds found. Please try again later.")

        # Calculate SIP amounts
        no_stepup_sip = calculate_sip(future_value, tenure)
        stepup_sip = calculate_sip(future_value, tenure, step_up_rate=10)

        st.subheader("SIP Amounts:")
        st.write(f"No Step-up SIP: ₹{no_stepup_sip:.2f} per month")
        st.write(f"Step-up SIP (10% annual increase): ₹{stepup_sip:.2f} per month")
    else:
        st.error("Please enter valid Goal Value and Tenure.")
