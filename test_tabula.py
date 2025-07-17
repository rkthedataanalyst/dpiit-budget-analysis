import pandas as pd

# Load the Excel file and skip the metadata/header rows
df = pd.read_excel("dpiit_budget.xlsx", sheet_name="Table 1", skiprows=5)

# Drop empty rows and columns
df.dropna(axis=0, how='all', inplace=True)
df.dropna(axis=1, how='all', inplace=True)

# Preview the cleaned data
print(df.head())

# Save as CSV
df.to_csv("dpiit_budget_cleaned.csv", index=False)
print("✅ Cleaned CSV saved successfully!")

