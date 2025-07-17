import pandas as pd
import re
import plotly.express as px

# Load the Excel file and skip the metadata/header rows
raw_df = pd.read_excel("dpiit_budget.xlsx", sheet_name="Table 1", skiprows=5, header=None)

# Drop empty rows and columns
raw_df.dropna(axis=0, how='all', inplace=True)
raw_df.dropna(axis=1, how='all', inplace=True)
raw_df.reset_index(drop=True, inplace=True)

# Combine first two rows to create multi-level columns
header1 = raw_df.iloc[0].fillna('')
header2 = raw_df.iloc[1].fillna('')
columns = [f"{str(h1).strip()}_{str(h2).strip()}" if str(h2).strip() else str(h1).strip() for h1, h2 in zip(header1, header2)]

# Set new columns and remove header rows from data
data = raw_df.iloc[2:].copy()
data.columns = columns

# Identify columns to melt: those matching '_<Type> <Year>'
budget_col_pattern = re.compile(r'_(Actual|Budget|Revised) (\d{4}-\d{4})')
budget_cols = [col for col in data.columns if budget_col_pattern.search(col)]

print("Columns to melt (budget columns):", budget_cols)

# Melt the DataFrame to long format
id_col = data.columns[0]
df_long = pd.melt(data, id_vars=[id_col], value_vars=budget_cols, var_name='Type_Year', value_name='Amount (₹ Cr)')

# Extract Budget Type and Year from 'Type_Year'
type_year = df_long['Type_Year'].str.extract(r'_(Actual|Budget|Revised) (\d{4}-\d{4})')
df_long['Budget Type'] = type_year[0]
df_long['Year'] = type_year[1]

# Rename columns
final_df = df_long.rename(columns={id_col: 'Scheme/Project Name'})[['Scheme/Project Name', 'Budget Type', 'Year', 'Amount (₹ Cr)']]

# Clean Amount column: remove commas, convert to float
final_df['Amount (₹ Cr)'] = final_df['Amount (₹ Cr)'].astype(str).str.replace(',', '').str.extract(r'([\d.]+)')[0]
final_df['Amount (₹ Cr)'] = pd.to_numeric(final_df['Amount (₹ Cr)'], errors='coerce')

# Drop rows with missing key info
final_df.dropna(subset=['Scheme/Project Name', 'Budget Type', 'Year', 'Amount (₹ Cr)'], how='any', inplace=True)

# Preview the cleaned data
print(final_df.head(10))

# Save as CSV
csv_path = "dpiit_budget_cleaned_structured_long.csv"
final_df.to_csv(csv_path, index=False)
print(f"✅ Structured long-format CSV saved successfully as {csv_path}!")

df = pd.read_csv('dpiit_budget_cleaned_structured_long.csv')

# Total budget by year
yearly = df.groupby('Year')['Amount (₹ Cr)'].sum().reset_index()
fig = px.bar(yearly, x='Year', y='Amount (₹ Cr)', title='Total Budget by Year')
fig.show()

top10 = df.groupby('Scheme/Project Name')['Amount (₹ Cr)'].sum().nlargest(10).reset_index()
fig = px.bar(top10, x='Scheme/Project Name', y='Amount (₹ Cr)', title='Top 10 Funded Projects')
fig.show()

trend = df.pivot_table(index='Year', columns='Scheme/Project Name', values='Amount (₹ Cr)', aggfunc='sum')
fig = px.line(trend, x=trend.index, y=trend.columns, title='Year-on-Year Trend')
fig.show()

est_actual = df[df['Budget Type'].isin(['Budget', 'Revised', 'Actual'])]
est_actual_grouped = est_actual.groupby(['Year', 'Budget Type'])['Amount (₹ Cr)'].sum().reset_index()
fig = px.bar(est_actual_grouped, x='Year', y='Amount (₹ Cr)', color='Budget Type', barmode='group', title='Estimate vs Actuals')
fig.show()

# Highest budget increase
df['Amount_prev'] = df.groupby('Scheme/Project Name')['Amount (₹ Cr)'].shift(1)
df['YoY_Growth'] = (df['Amount (₹ Cr)'] - df['Amount_prev']) / df['Amount_prev'] * 100
max_increase = df.loc[df['YoY_Growth'].idxmax()]

# Actual vs Estimate
comparison = df.pivot_table(index=['Scheme/Project Name', 'Year'], columns='Budget Type', values='Amount (₹ Cr)')
comparison['Overspending'] = comparison['Actual'] - comparison['Budget']
overspending = comparison[comparison['Overspending'] > 0]
underfunded = comparison[comparison['Overspending'] < 0]
