'''2. Otázka.
Který den v týdnu je nejsilnější na počet objednávek?'''

# Nejdřive importujeme knihovny a data pro jejich zpracování
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt


data = pd.ExcelFile('Data.xlsx') #načteme excel soubor
#print(data.sheet_names) #vypíše názvy listů v excelu (pro kontrolu)
df_transactions = data.parse('Transactions') #načte list Transactions
df_products = data.parse('Products') #načte list Products
df_merged = pd.merge(df_transactions, df_products, on='Product name', how='inner') #sloučí listy podle názvu produktu
df_merged['Weekday'] = df_merged['Date'].dt.day_name() #přidáme sloupec s dnem v týdnu
df_merged['Revenue'] = df_merged['Price'] * df_merged['Quantity'] #přidáme sloupec s výpočtem obratu
print("Počet transakci za celé období:", df_merged['Transaction ID'].nunique()) #vypíše počet transakci za celé období

# Seřadíme dny v týdnu podle počtu transakci, množství prodaných produktů a celkového obratu
weekday_sales = df_merged.groupby('Weekday').agg(
    Total_Transactions=('Transaction ID', 'nunique'),
    Total_Quantity=('Quantity', 'sum'),
    Total_Revenue=('Revenue', 'sum')
).reset_index()
print(weekday_sales.sort_values(by=['Total_Transactions','Total_Quantity'], ascending=False))


# Vytvoříme grafy
fig, ax = plt.subplots(3, 1, figsize=(15, 13))
weekday_sales.plot(kind='bar', x='Weekday', y='Total_Transactions', ax=ax[0], color='skyblue')
ax[0].set_title('Počet transakcí v jednotlivé dny v týdnu')
ax[0].set_ylabel('Počet transakcí')
ax[0].set_xlabel('Den v týdnu')

weekday_sales.plot(kind='bar', x='Weekday', y='Total_Quantity', ax=ax[1], color='lightgreen')
ax[0].set_title('Počet prodaných produktů v jednotlivé dny v týdnu')
ax[1].set_ylabel('Počet prodaných produktů')
ax[1].set_xlabel('Den v týdnu')

weekday_sales.plot(kind='bar', x='Weekday', y='Total_Revenue', ax=ax[2], color='salmon')
ax[0].set_title('Celkový obrat v jednotlivé dny v týdnu')
ax[2].set_ylabel('Celkový obrat')
ax[2].set_xlabel('Den v týdnu')

plt.show()


days_order = weekday_sales.sort_values(by=['Total_Transactions', 'Total_Quantity'], ascending=False)['Weekday']
weekday_sales['Weekday'] = pd.Categorical(weekday_sales['Weekday'], categories=days_order, ordered=True)
weekday_sales = weekday_sales.sort_values('Weekday')

# Vizualizace na jednom grafu
fig, ax = plt.subplots(figsize=(12, 8))

# Šířka sloupců
bar_width = 0.2
x = range(len(weekday_sales))

# Sloupce pro jednotlivé metriky
ax.bar(x, weekday_sales['Total_Transactions'], width=bar_width, label='Počet transakcí', color='skyblue')
ax.bar([p + bar_width for p in x], weekday_sales['Total_Quantity'], width=bar_width, label='Počet prodaných produktů', color='lightgreen')
#ax.bar([p + bar_width * 2 for p in x], weekday_sales['Total_Revenue'], width=bar_width, label='Celkový obrat', color='salmon')

# Nadpisy a popisky
ax.set_title('Analýza prodeje podle dne v týdnu')
ax.set_xlabel('Den v týdnu')
ax.set_ylabel('Hodnota')
ax.set_xticks([p + bar_width for p in x])
ax.set_xticklabels(weekday_sales['Weekday'])
ax.legend()

# Anotace
for i in range(len(weekday_sales)):
    ax.text(i, weekday_sales['Total_Transactions'].iloc[i] + 1, str(weekday_sales['Total_Transactions'].iloc[i]), ha='center')
    ax.text(i + bar_width, weekday_sales['Total_Quantity'].iloc[i] + 1, str(weekday_sales['Total_Quantity'].iloc[i]), ha='center')
    #ax.text(i + bar_width * 2, weekday_sales['Total_Revenue'].iloc[i] + 1, f"{weekday_sales['Total_Revenue'].iloc[i]:,.0f} Kč", ha='center')

plt.tight_layout()
plt.show()


