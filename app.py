import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# Load Data
# ------------------------------
@st.cache_data
def load_data():
    xls = pd.ExcelFile("lulu_mall_synthetic_data.xlsx")
    customers = pd.read_excel(xls, "Customer_Demographics")
    loyalty = pd.read_excel(xls, "Loyalty_Program")
    sales = pd.read_excel(xls, "Sales_Transactions")
    ads = pd.read_excel(xls, "Advertisement_Spend")
    return customers, loyalty, sales, ads

customers, loyalty, sales, ads = load_data()

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Lulu Mall Dashboard", layout="wide")
st.title("🏬 Lulu Mall Dubai – Analytics Dashboard")

# Sidebar Navigation
section = st.sidebar.radio("📊 Select Section", 
                           ["Sales Insights", "Customer Insights", "Loyalty Program", "Advertisement Spend"])

# ------------------------------
# Sales Insights
# ------------------------------
if section == "Sales Insights":
    st.header("💰 Sales Insights")

    total_sales = sales["Total_Amount"].sum()
    avg_basket = sales["Total_Amount"].mean()
    total_txns = sales.shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales (AED)", f"{total_sales:,.0f}")
    col2.metric("Avg. Basket Size (AED)", f"{avg_basket:,.2f}")
    col3.metric("Total Transactions", total_txns)

    # Monthly sales trend
    monthly_sales = sales.groupby(sales["Date"].dt.to_period("M"))["Total_Amount"].sum().reset_index()
    monthly_sales["Date"] = monthly_sales["Date"].astype(str)
    fig1 = px.line(monthly_sales, x="Date", y="Total_Amount", title="Monthly Sales Trend (AED)")
    st.plotly_chart(fig1, use_container_width=True)

    # Category-wise sales
    fig2 = px.pie(sales, names="Product_Category", values="Total_Amount", title="Sales by Category")
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Customer Insights
# ------------------------------
elif section == "Customer Insights":
    st.header("👥 Customer Insights")

    fig3 = px.histogram(customers, x="Age", nbins=20, title="Age Distribution of Customers")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.bar(customers["Nationality"].value_counts().reset_index(),
                  x="index", y="Nationality", title="Customers by Nationality",
                  labels={"index": "Nationality", "Nationality": "Count"})
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.bar(customers["Location"].value_counts().reset_index(),
                  x="index", y="Location", title="Customers by Location",
                  labels={"index": "Location", "Location": "Count"})
    st.plotly_chart(fig5, use_container_width=True)

# ------------------------------
# Loyalty Program
# ------------------------------
elif section == "Loyalty Program":
    st.header("🎯 Loyalty Program Insights")

    active_loyalty = loyalty[loyalty["Active_Status"] == "Yes"].shape[0]
    total_loyalty = loyalty.shape[0]

    col1, col2 = st.columns(2)
    col1.metric("Active Loyalty Members", active_loyalty)
    col2.metric("Total Loyalty Members", total_loyalty)

    fig6 = px.pie(loyalty, names="Tier", title="Loyalty Tier Distribution")
    st.plotly_chart(fig6, use_container_width=True)

    fig7 = px.scatter(loyalty, x="Points_Earned", y="Points_Redeemed", color="Tier",
                      title="Points Earned vs Redeemed")
    st.plotly_chart(fig7, use_container_width=True)

# ------------------------------
# Advertisement Spend
# ------------------------------
elif section == "Advertisement Spend":
    st.header("📢 Advertisement Spend & ROI")

    fig8 = px.bar(ads, x="Date", y="Budget_Spent", color="Category", 
                  title="Monthly Advertisement Spend by Category")
    st.plotly_chart(fig8, use_container_width=True)

    fig9 = px.line(ads, x="Date", y="ROI", color="Category",
                   title="Advertisement ROI by Category")
    st.plotly_chart(fig9, use_container_width=True)
