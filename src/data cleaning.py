# Reconstruct a larger version of the final structured CSV from stored structured values in chunks
# For demonstration, we'll add more representative rows from key findings

data_full = [
    # Secretariat (Establishment)
    {"Scheme_Name": "Secretariat", "Year": "FY2021-22", "Budget_Type": "Actual", "Amount_Cr": 114.18, "Allocation_Trend": "Up", "YoY_Growth": "", "Category": "Establishment", "Relevant_Notes": "Core administration of DPIIT"},
    {"Scheme_Name": "Secretariat", "Year": "FY2022-23", "Budget_Type": "Budget", "Amount_Cr": 114.36, "Allocation_Trend": "Up", "YoY_Growth": "0.2%", "Category": "Establishment", "Relevant_Notes": ""},
    {"Scheme_Name": "Secretariat", "Year": "FY2023-24", "Budget_Type": "Budget", "Amount_Cr": 202.10, "Allocation_Trend": "Up", "YoY_Growth": "76.7%", "Category": "Establishment", "Relevant_Notes": ""},
    {"Scheme_Name": "Secretariat", "Year": "FY2024-25", "Budget_Type": "Budget", "Amount_Cr": 232.81, "Allocation_Trend": "Up", "YoY_Growth": "15.2%", "Category": "Establishment", "Relevant_Notes": ""},

    # Intellectual Property
    {"Scheme_Name": "Intellectual_Property_Promotion", "Year": "FY2024-25", "Budget_Type": "Budget", "Amount_Cr": 318.02, "Allocation_Trend": "Down", "YoY_Growth": "-3.3%", "Category": "Establishment", "Relevant_Notes": "CGPDTM, CIPAM, IP awareness"},

    # Fund of Funds for Startups
    {"Scheme_Name": "Fund_of_Funds_for_Startups", "Year": "FY2022-23", "Budget_Type": "Budget", "Amount_Cr": 1330.00, "Allocation_Trend": "Up", "YoY_Growth": "", "Category": "Central Sector Scheme", "Relevant_Notes": "Startup India – SIDBI fund"},
    {"Scheme_Name": "Fund_of_Funds_for_Startups", "Year": "FY2024-25", "Budget_Type": "Budget", "Amount_Cr": 1470.00, "Allocation_Trend": "Up", "YoY_Growth": "47.0%", "Category": "Central Sector Scheme", "Relevant_Notes": ""},

    # NICDIT
    {"Scheme_Name": "NICDIT (Industrial Corridors)", "Year": "FY2021-22", "Budget_Type": "Actual", "Amount_Cr": 1104.68, "Allocation_Trend": "Up", "YoY_Growth": "", "Category": "Central Sector Scheme", "Relevant_Notes": ""},
    {"Scheme_Name": "NICDIT (Industrial Corridors)", "Year": "FY2024-25", "Budget_Type": "Budget", "Amount_Cr": 500.00, "Allocation_Trend": "Down", "YoY_Growth": "-66.7%", "Category": "Central Sector Scheme", "Relevant_Notes": ""},

    # GST Refund
    {"Scheme_Name": "GST_Refund_NE_Himalayan", "Year": "FY2024-25", "Budget_Type": "Budget", "Amount_Cr": 1382.35, "Allocation_Trend": "Down", "YoY_Growth": "-21.2%", "Category": "Central Sector Scheme", "Relevant_Notes": "Incentives for NE/Himalayan states"},

    # Startup Seed Fund
    {"Scheme_Name": "Startup_India_Seed_Fund", "Year": "FY2024-25", "Budget_Type": "Budget", "Amount_Cr": 175.00, "Allocation_Trend": "Up", "YoY_Growth": "9.4%", "Category": "Central Sector Scheme", "Relevant_Notes": "Seed fund support for MSMEs/startups"},

    # PLI for White Goods
    {"Scheme_Name": "PLI_White_Goods", "Year": "FY2024-25", "Budget_Type": "Budget", "Amount_Cr": 298.02, "Allocation_Trend": "Up", "YoY_Growth": "358.5%", "Category": "Central Sector Scheme", "Relevant_Notes": "PLI incentives for manufacturing"},
]

# Create DataFrame
df_full = pd.DataFrame(data_full)

# Save to CSV
full_csv_path = "/mnt/data/dpiit_budget_analysis_full.csv"
df_full.to_csv(full_csv_path, index=False)

full_csv_path
import pandas as pd
import plotly.express as px 

# Load the cleaned structured long-format CSV
df = pd.read_csv('dpiit_budget_cleaned_structured_long.csv')    



# Total budget by year
yearly = df.groupby('Year')['Amount (₹ Cr)'].sum().reset_index()
