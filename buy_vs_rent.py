import streamlit as st
import numpy as np

st.title("Buy vs Rent Calculator")

# Inputs
st.sidebar.header("Inputs")
rent = st.sidebar.number_input("Monthly Rent ($)", value=6700, step=100)
home_price = st.sidebar.number_input("Home Price ($)", value=2500000, step=10000)
rent_increase = st.sidebar.slider("Annual Rent Increase (%)", 0.0, 5.0, 2.0) / 100
home_appreciation = st.sidebar.slider("Annual Home Appreciation (%)", 0.0, 5.0, 1.0) / 100
investment_return = st.sidebar.slider("Investment Return (Opportunity Cost, %)", 0.0, 10.0, 5.0) / 100
property_tax_rate = st.sidebar.slider("Property Tax Rate (%)", 0.0, 3.0, 1.5) / 100
insurance_rate = st.sidebar.slider("Home Insurance Rate (%)", 0.0, 1.0, 0.3) / 100
maintenance_rate = st.sidebar.slider("Maintenance Cost Rate (%)", 0.0, 2.0, 1.0) / 100
transaction_cost = st.sidebar.slider("Transaction Cost (Buy+Sell, %)", 0.0, 10.0, 7.0) / 100
holding_period = st.sidebar.slider("Holding Period (Years)", 1, 30, 10)

# Mortgage inputs
st.sidebar.header("Mortgage Options")
down_payment_pct = st.sidebar.slider("Down Payment (%)", 0.0, 100.0, 100.0) / 100
mortgage_rate = st.sidebar.slider("Mortgage Rate (%)", 0.0, 10.0, 6.5) / 100
loan_term_years = st.sidebar.slider("Loan Term (Years)", 5, 40, 30)

# Derived mortgage values
down_payment = home_price * down_payment_pct
loan_amount = home_price - down_payment
monthly_rate = mortgage_rate / 12
n_payments = loan_term_years * 12
if loan_amount > 0:
    monthly_mortgage_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
else:
    monthly_mortgage_payment = 0

# Annualized costs
annual_rent = rent * 12
annual_property_tax = home_price * property_tax_rate
annual_insurance = home_price * insurance_rate
annual_maintenance = home_price * maintenance_rate
annual_ownership_cost = annual_property_tax + annual_insurance + annual_maintenance
annual_mortgage_payment = monthly_mortgage_payment * 12

def npv_of_rent(r0, growth, discount, years):
    return sum(r0 * (1 + growth)**t / (1 + discount)**t for t in range(1, years + 1))

def owning_vs_renting(home_price, appreciation, discount_rate, years):
    npv_costs = 0
    for t in range(1, years + 1):
        yearly_cost = annual_ownership_cost + (annual_mortgage_payment if t <= loan_term_years else 0)
        npv_costs += yearly_cost / (1 + discount_rate)**t
    future_home_value = home_price * (1 + appreciation)**years
    net_sale_value = future_home_value * (1 - transaction_cost)
    net_gain = net_sale_value - home_price
    npv_net_gain = net_gain / (1 + discount_rate)**years
    return npv_costs - npv_net_gain

rent_npv = npv_of_rent(annual_rent, rent_increase, investment_return, holding_period)
own_npv = owning_vs_renting(home_price, home_appreciation, investment_return, holding_period)
diff = rent_npv - own_npv

# Results
st.subheader("Results")
st.write(f"**NPV Cost of Renting:** ${rent_npv:,.0f}")
st.write(f"**NPV Cost of Owning:** ${own_npv:,.0f}")

if diff > 0:
    st.success(f"Renting is cheaper by ${diff:,.0f} in present value terms.")
elif diff < 0:
    st.success(f"Buying is cheaper by ${-diff:,.0f} in present value terms.")
else:
    st.info("Renting and buying are approximately equal in cost.")
