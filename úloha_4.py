import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.ExcelFile('Data.xlsx') # načteme excel soubor
#print(data.sheet_names) # vypíše názvy listů v excelu (pro kontrolu)
df_transactions = data.parse('Transactions') # načte list Transactions
df_products = data.parse('Products') # načte list Products
df_merged = pd.merge(df_transactions, df_products, on='Product name', how='inner') # sloučí listy podle názvu produktu
df_merged['Month'] = df_merged['Date'].dt.to_period('M')
df_merged['Week'] = df_merged['Date'].dt.isocalendar().week # přidáme sloupec s týdnem
df_merged['Revenue'] = df_merged['Price'] * df_merged['Quantity'] # přidáme sloupec s výpočtem obratu

budget_increase_date = pd.Timestamp('2022-03-18') #datum zvýšení rozpočtu na online marketing



sales_before = df_merged[df_merged['Date'] < budget_increase_date].groupby('Week')['Revenue'].sum() # obrat před zvýšením rozpočtu
sales_after = df_merged[df_merged['Date'] >= budget_increase_date].groupby('Week')['Revenue'].sum() # obrat po zvýšení rozpočtu

# Porovnáme obrat před a po zvýšení rozpočtu
sales_comparison = pd.DataFrame({'Obrat před': sales_before, 'Obrat po': sales_after}).fillna(0) #vytvoříme dataframe pro porovnání
average_sales_before = sales_comparison[sales_comparison['Obrat před']>0]['Obrat před'].mean() #spočítáme průměrný obrat (za týden) před zvýšením rozpočtu
average_sales_after = sales_comparison[sales_comparison['Obrat po'] > 0]['Obrat po'].mean() #spočítáme průměrný obrat (za týden) po zvýšení rozpočtu
# Vypíšeme výsledky
print("Srovnání prodejů před a po navýšení rozpočtu na online marketing podle týdnů:")
print(sales_comparison)
print(f"Průměr obratu za týden před zvýšením rozpočtu: {average_sales_before:.0f}")
print(f"Průměr obratu za týden po zvýšení rozpočtu: {average_sales_after:.0f}")

# Vytvoříme df pro porovnání prodejů před a po zvýšení rozpočtu a rozdělíme to podle kategorií
sales_before = df_merged[df_merged['Date'] < budget_increase_date].groupby(['Week', 'Category'])['Revenue'].sum().unstack(fill_value=0)
sales_after = df_merged[df_merged['Date'] >= budget_increase_date].groupby(['Week', 'Category'])['Revenue'].sum().unstack(fill_value=0)
sales_comparison = pd.concat([sales_before.add_suffix(' (Před)'), sales_after.add_suffix(' (Po)')], axis=1) # sloučíme data pro porovnání

'''
# Выводим результаты (pro kontrolu)
print("Сравнение продаж по неделям и категориям:")
print(sales_comparison)
'''

total_sales_before = df_merged[df_merged['Date'] < budget_increase_date].groupby('Week')['Revenue'].sum()
total_sales_after = df_merged[df_merged['Date'] >= budget_increase_date].groupby('Week')['Revenue'].sum()

# Vytvoříme grafy pro srovnání prodejů před a po zvýšení rozpočtu
fig, ax = plt.subplots(2, 1, figsize=(15, 10))

# Graf sravnění prodejů podle kategorií během týdnů
sales_comparison.plot(kind='bar', ax=ax[0])
ax[0].set_title('Porivnání prodejů podle kategorií')
ax[0].set_xlabel('')
ax[0].set_ylabel('Obrat')
ax[0].legend(title='Kategorie')
ax[0].set_xticklabels(sales_comparison.index, rotation=45)

# Graf celkového obratu během týdnů
total_sales = pd.DataFrame({'Celkový obrat (Před)': total_sales_before, 'Celkový obrat (Po)': total_sales_after})
total_sales.plot(kind='bar', ax=ax[1])
ax[1].set_title('Celkový obrat během týdnů')
ax[1].set_xlabel('Číslo týdne')
ax[1].set_ylabel('Obrat')
ax[1].set_xticklabels(total_sales.index, rotation=45)

plt.tight_layout()
plt.show()

