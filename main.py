#importujeme data a knihovny pro zpracování dat
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
file = 'Data.xlsx'
data = pd.ExcelFile(file)
print(data.sheet_names) #vypíše názvy listů v excelu
df1 = data.parse('Transactions') #načte list Transactions
df2 = data.parse('Products') #načte list Products
df_merged = pd.merge(df1, df2, on='Product name', how='inner') #sloučí listy podle názvu produktu
print(df_merged.info()) #vypíše informace o sloučeném listu

#vypíše unikátní produkty
unique_products = df_merged['Product name'].unique()
print('Počet produktů ID je: ', unique_products.size, ' a jsou to: ', unique_products)

#vypíše unikátní kategorie
unique_categories = df_merged['Category'].unique()
print('Počet kategorií je: ', unique_categories.size, ' a jsou to: ', unique_categories)

#přidáme sloupec s výpočtem obratu
df_merged['Revenue'] = df_merged['Price'] * df_merged['Quantity']

#přídáme sloupec s rozdělením času na měsíce
df_merged['Month'] = df_merged['Date'].dt.to_period('M')

#sgrupirujeme data podle měsíce a kategorie a spočítáme obrat
monthly_revenue = df_merged.groupby(['Month', 'Category'])['Revenue'].sum().reset_index()

total_revenue = monthly_revenue.groupby('Month')['Revenue'].sum().reset_index()
total_revenue.rename(columns={'Revenue': 'Total Revenue'}, inplace=True)
monthly_revenue = monthly_revenue.merge(total_revenue, on='Month')
monthly_revenue['Percentage'] = (monthly_revenue['Revenue'] / monthly_revenue['Total Revenue']) * 100

#pootočime dataset pro dnadnejší zpracování (pivot)
monthly_revenue_pivot = monthly_revenue.pivot(index='Month', columns='Category', values='Revenue')
pivot_percentage = monthly_revenue.pivot(index='Month', columns='Category', values='Percentage')

#pokusime vizualizovat data
plt.figure(figsize=(12, 6))
for category in monthly_revenue_pivot.columns:
    plt.plot(monthly_revenue_pivot.index.astype(str), monthly_revenue_pivot[category], marker='o', label=category)

plt.title('Monthly Revenue by Category')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)

for i, row in monthly_revenue.iterrows():
    month_str = row['Month'].strftime('%Y-%m')  # měníme typ data na string
    annotation_text = f"{row['Percentage']:.1f}% ({row['Revenue']:.2f})"
    plt.annotate(annotation_text,
                 (month_str, row['Revenue']),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')

plt.legend(title='Category')
plt.grid()
plt.tight_layout()
plt.show()