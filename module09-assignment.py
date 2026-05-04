# Module 9 Assignment: Introduction to Data Analysis with Pandas
# GlobalTech Sales Analysis

import pandas as pd
import numpy as np

print("=" * 60)
print("GLOBALTECH QUARTERLY SALES ANALYSIS")
print("=" * 60)

from io import StringIO

csv_content = """Date,Region,Store,Category,Product,Units,Unit_Price,Total_Sales,Promotion
2024-01-15,North America,NA001,Smartphones,PhoneX,12,899.99,10799.88,No
2024-01-18,Europe,EU002,Computers,LaptopPro,8,1299.99,10399.92,Yes
2024-01-20,Asia,AS001,Audio,WirelessEarbuds,25,149.99,3749.75,No
2024-01-22,North America,NA002,Wearables,SmartWatch,15,249.99,3749.85,No
2024-01-25,Latin America,LA001,Smartphones,PhoneX,7,899.99,6299.93,Yes
2024-01-27,Europe,EU001,Accessories,PhoneCase,35,24.99,874.65,No
2024-01-30,Asia,AS002,Smartphones,PhoneSE,18,499.99,8999.82,No
2024-02-02,North America,NA001,Computers,LaptopPro,6,1299.99,7799.94,No
2024-02-05,Europe,EU002,Wearables,SmartWatch,20,249.99,4999.80,Yes
2024-02-08,North America,NA003,Audio,WirelessEarbuds,30,149.99,4499.70,Yes
2024-02-10,Asia,AS001,Accessories,ChargingCable,45,19.99,899.55,No
2024-02-12,Latin America,LA001,Computers,TabletBasic,12,399.99,4799.88,No
2024-02-15,North America,NA002,Smartphones,PhoneSE,14,499.99,6999.86,No
2024-02-18,Europe,EU001,Audio,BlueSpeaker,22,79.99,1759.78,Yes
2024-02-20,Asia,AS002,Wearables,FitnessTracker,28,129.99,3639.72,No
2024-02-22,North America,NA001,Accessories,PhoneCase,50,24.99,1249.50,Yes
2024-02-25,Latin America,LA002,Smartphones,PhoneX,9,,8099.91,No
2024-02-28,Europe,EU002,Computers,LaptopBasic,10,899.99,8999.90,No
2024-03-02,North America,NA003,Wearables,FitnessTracker,,129.99,2599.80,Yes
2024-03-05,Asia,AS001,Smartphones,PhoneSE,15,499.99,7499.85,No
2024-03-08,Europe,EU001,Accessories,ChargingCable,60,19.99,1199.40,Yes
2024-03-10,North America,NA002,Computers,TabletPro,7,599.99,4199.93,No
2024-03-12,Latin America,LA001,Audio,WirelessEarbuds,18,149.99,2699.82,No
2024-03-15,North America,NA001,Wearables,SmartWatch,12,249.99,2999.88,No
2024-03-18,Europe,EU002,Smartphones,PhoneX,11,899.99,9899.89,Yes
2024-03-20,Asia,AS002,Computers,LaptopPro,6,1299.99,7799.94,No
2024-03-22,North America,NA001,Audio,BlueSpeaker,25,79.99,1999.75,No
2024-03-25,Latin America,LA002,Accessories,PhoneCase,40,,999.60,No
"""

sales_data_csv = StringIO(csv_content)

# load data
sales_df = pd.read_csv(sales_data_csv)

# quick look
print(sales_df.head())
sales_df.info()
print(sales_df.shape)
print(sales_df.describe())

# select some columns
print(sales_df[["Product", "Units", "Total_Sales"]])

# basic calcs
total_units = sales_df["Units"].sum()
total_revenue = sales_df["Total_Sales"].sum()
avg_unit_price = sales_df["Unit_Price"].mean()

# filters
na_sales = sales_df[sales_df["Region"] == "North America"]
high_volume_sales = sales_df[sales_df["Units"] > 20]
phonex_promo = sales_df[(sales_df["Product"] == "PhoneX") & (sales_df["Promotion"] == "Yes")]
feb_sales = sales_df[sales_df["Date"].str.startswith("2024-02")]

# analysis
best_product = sales_df.groupby("Product")["Total_Sales"].sum().idxmax()
sales_by_region = sales_df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
avg_units_by_category = sales_df.groupby("Category")["Units"].mean()

promo_comparison = {
    "promo_avg_sales": sales_df[sales_df["Promotion"] == "Yes"]["Total_Sales"].mean(),
    "no_promo_avg_sales": sales_df[sales_df["Promotion"] == "No"]["Total_Sales"].mean(),
    "promo_total_revenue": sales_df[sales_df["Promotion"] == "Yes"]["Total_Sales"].sum(),
    "no_promo_total_revenue": sales_df[sales_df["Promotion"] == "No"]["Total_Sales"].sum()
}

# missing values
missing_counts = sales_df.isnull().sum()
missing_percentages = (sales_df.isnull().sum() / len(sales_df)) * 100

# more analysis
cat_region = sales_df.groupby(["Region", "Category"])["Total_Sales"].sum()
top_categories_by_region = cat_region.groupby(level=0).idxmax().apply(lambda x: x[1])

avg_price_by_category = sales_df.groupby("Category")["Unit_Price"].mean()

product_totals = sales_df.groupby("Product")["Total_Sales"].sum()
product_revenue_analysis = pd.DataFrame({
    "total_revenue": product_totals,
    "percentage": (product_totals / total_revenue) * 100
})

print("\n" + "=" * 60)
print("GLOBALTECH Q1 2024 SALES ANALYSIS REPORT")
print("=" * 60)

avg_sale = sales_df["Total_Sales"].mean()

print("\nOverall Performance:")
print(f"- Total Revenue: ${total_revenue:,.2f}")
print(f"- Total Units Sold: {int(total_units)}")
print(f"- Average Sale Value: ${avg_sale:,.2f}")

print("\nRegional Performance:")
for r, v in sales_by_region.items():
    print(f"{r}: ${v:,.2f}")

print("\nCategory Performance:")
for c in avg_units_by_category.index:
    print(f"{c}: Avg Units: {avg_units_by_category[c]:.1f}, Avg Price: ${avg_price_by_category[c]:.2f}")

print("\nPromotion Effectiveness:")
print(f"- Promoted Items Avg Sale: ${promo_comparison['promo_avg_sales']:.2f}")
print(f"- Non-Promoted Items Avg Sale: ${promo_comparison['no_promo_avg_sales']:.2f}")
print(f"- Revenue from Promotions: ${promo_comparison['promo_total_revenue']:,.2f}")

missing_cols = missing_counts[missing_counts > 0].index.tolist()
total_missing = int(missing_counts.sum())

print("\nData Quality Report:")
print(f"- Missing Values Found: {missing_cols}")
print(f"- Total Missing Entries: {total_missing}")

print("\nKEY BUSINESS RECOMMENDATIONS:")
print("1. smartphones are clearly bringing in the most money so prob focus inventory there esp phonex")
print("2. north america + europe are strongest regions so marketing spend should go there")
print("3. promos bring in revenue but avg sale is lower so might be discounting too hard")
