"""1. Otázka.
 Na jaké kategorii produktů máme největší obrat?
A zajímalo by mě i jestli se to v jednotlivých měsících mění."""

# Nejdřive importujeme knihovny a data pro jejich zpracování
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from adjustText import adjust_text

data = pd.ExcelFile('Data.xlsx') #načteme excel soubor
#print(data.sheet_names) #vypíše názvy listů v excelu (pro kontrolu]
df1 = data.parse('Transactions') #načte list Transactions
df2 = data.parse('Products') #načte list Products
df_merged = pd.merge(df1, df2, on='Product name', how='inner') #sloučí listy podle názvu produktu
#print(df_merged.info()) #vypíše informace o sloučeném listu (pro kontrolu)

# Vypíšeme unikátní produkty
unique_products = df_merged['Product name'].unique()
print('Počet produktů ID je: ', unique_products.size, ' a jsou to: ', unique_products)

# Vypíšeme unikátní kategorie
unique_categories = df_merged['Category'].unique()
print('Počet kategorií je: ', unique_categories.size, ' a jsou to: ', unique_categories)

# Přidáme sloupec s výpočtem obratu
df_merged['Revenue'] = df_merged['Price'] * df_merged['Quantity']

# Přídáme sloupec s rozdělením transakci na měsíce
df_merged['Month'] = df_merged['Date'].dt.to_period('M')

# Sloučíme data podle měsíce a kategorie a spočítáme měsiční obrat každé kategorie
monthly_revenue = df_merged.groupby(['Month', 'Category'])['Revenue'].sum().reset_index()
#print(monthly_revenue) #vypíše měsiční obrat každé kategorie za každý měsíc (pro kontrolu)

# Spočítáme celkový měsiční obrat za každý měsíc
total_revenue = monthly_revenue.groupby('Month')['Revenue'].sum().reset_index() # spočítáme celkový měsiční obrat za kazdý měsíc
total_revenue.rename(columns={'Revenue': 'Total Revenue'}, inplace=True) # přejmenujeme sloupec
#print(total_revenue) #vypíše celkový měsiční obrat za každý měsíc (pro kontrolu)
monthly_revenue = monthly_revenue.merge(total_revenue, on='Month') #sloučíme data

# Přidáme sloupec s procentuálním rozdělením obratu pro lepší porovnání
monthly_revenue['Percentage'] = (monthly_revenue['Revenue'] / monthly_revenue['Total Revenue']) * 100
print(monthly_revenue[['Month', 'Category', 'Revenue', 'Percentage']]) #vypíše měsiční obrat a procentuální rozdělení obratu každé kategorie za každý měsíc


#pootočime dataset pro dnadnejší zpracování (pivot)
monthly_revenue_pivot = monthly_revenue.pivot(index='Month', columns='Category', values='Revenue')
pivot_percentage = monthly_revenue.pivot(index='Month', columns='Category', values='Percentage')



# Hrubá vizualizace (bez anotací)
plt.figure(figsize=(18, 10))
for category in monthly_revenue_pivot.columns:
    plt.plot(monthly_revenue_pivot.index.astype(str),
             monthly_revenue_pivot[category],
             marker='o', label=category)

plt.title('Měsíční obrat každé kategorií')
plt.xlabel('Měsíc')
plt.ylabel('Obrat')
plt.xticks(rotation=45)

# Přidáme popisky k jednotlivým bodům (anotace)
y_values = {}

for i, row in monthly_revenue.iterrows():
    month_str = row['Month'].strftime('%Y-%m')  # měníme typ data na string ve formátu 'YYYY-MM'
    percentage = f"{row['Percentage']:.0f}%"  # zaokrouhlíme na celé procenta
    revenue = f"({row['Revenue']:.0f} Kč)"  # formátujeme na ceny v Kč
    annotation_text = f"{percentage} {revenue}"

    y_offset = 10
    if month_str in y_values:
        for previous_value in y_values[month_str]:
            if abs(row['Revenue'] - previous_value) < 200:
                y_offset += 10

    plt.annotate(annotation_text,
                (month_str, row['Revenue']),
                textcoords="offset points",
                xytext=(5, y_offset),
                ha='left')
    if month_str not in y_values:
        y_values[month_str] = []
    y_values[month_str].append(row['Revenue'])

plt.legend(title='Category')
plt.show()