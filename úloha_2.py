'''2. Otázka.
Který den v týdnu je nejsilnější na počet objednávek?'''

# Nejdřive importujeme knihovny a data pro jejich zpracování
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.ExcelFile('Data.xlsx') #načteme excel soubor
#print(data.sheet_names) #vypíše názvy listů v excelu (pro kontrolu)
df_transactions = data.parse('Transactions') #načte list Transactions
df_products = data.parse('Products') #načte list Products
df_merged = pd.merge(df_transactions, df_products, on='Product name', how='inner') #sloučí listy podle názvu produktu
df_merged['Weekday'] = df_merged['Date'].dt.day_name() #přidáme sloupec s dnem v týdnu
df_merged['Week'] = df_merged['Date'].dt.isocalendar().week #přidáme sloupec s týdnem
df_merged['Revenue'] = df_merged['Price'] * df_merged['Quantity'] #přidáme sloupec s výpočtem obratu

print("Počet transakci za celé období:", df_merged['Transaction ID'].nunique()) #vypíše počet transakci za celé období

# Seřadíme dny v týdnu podle počtu transakci, množství prodaných produktů a celkového obratu
weekday_sales = df_merged.groupby('Weekday').agg(
    Total_Transactions=('Transaction ID', 'nunique'),
    Total_Quantity=('Quantity', 'sum'),
    Total_Revenue=('Revenue', 'sum')
    ).reset_index()
print(weekday_sales.sort_values(by=['Total_Transactions','Total_Quantity'], ascending=False))


# 1. graf uděláme pro obecný přehled množství objednávek, prodaných produktů a celkového obratu

# Nastávíme pořadí dnů (dny v týdnu), můžeme pak měnit bud podle pořadí transakcí nebo množství prodaných produktů, nebo od Pondělka do Neděle
days_order = weekday_sales.sort_values(by=['Total_Transactions', 'Total_Quantity'], ascending=False)['Weekday'] # nastavime podle zadani (počtu transakcí)
weekday_sales['Weekday'] = pd.Categorical(weekday_sales['Weekday'], categories=days_order, ordered=True)
weekday_sales = weekday_sales.sort_values('Weekday')

fig, ax = plt.subplots(3, 1, figsize=(15, 13)) # vytvoříme 3 grafy pod sebou
weekday_sales.plot(kind='bar', y='Total_Transactions', ax=ax[0], color='skyblue')
ax[0].set_xticklabels(weekday_sales['Weekday'], rotation=0)
weekday_sales.plot(kind='bar', y='Total_Quantity', ax=ax[1], color='lightgreen')
ax[1].set_xticklabels(weekday_sales['Weekday'], rotation=0)
weekday_sales.plot(kind='bar', y='Total_Revenue', ax=ax[2], color='salmon')
ax[2].set_xticklabels(weekday_sales['Weekday'], rotation=0)
plt.show()


# 2. graf uděláme pro porovnání počtu transakcí a množství prodaných produktů na jednom grafu
fig, ax = plt.subplots(figsize=(12, 8))

# Šířka sloupců
bar_width = 0.2
x = range(len(weekday_sales))

# Sloupce pro jednotlivé metriky
ax.bar(x, weekday_sales['Total_Transactions'], width=bar_width, label='Total_Transactions', color='skyblue')
ax.bar([p + bar_width for p in x], weekday_sales['Total_Quantity'], width=bar_width, label='Total_Quantity', color='lightgreen')

# Nadpisy a popisky
ax.set_title('Analýza prodeje podle dne v týdnu')
ax.set_xticks([p + bar_width for p in x])
ax.set_xticklabels(weekday_sales['Weekday'])
ax.legend()

# Anotace
for i in range(len(weekday_sales)):
    ax.text(i, weekday_sales['Total_Transactions'].iloc[i] + 1, str(weekday_sales['Total_Transactions'].iloc[i]), ha='center')
    ax.text(i + bar_width, weekday_sales['Total_Quantity'].iloc[i] + 1, str(weekday_sales['Total_Quantity'].iloc[i]), ha='center')

plt.show()

# 3. graf uděláme ve stylu heatmapy pro počet transakcí podle týdne a dne v týdnu

weekly_sales = df_merged.groupby(['Week', 'Weekday'])['Transaction ID'].nunique().unstack(fill_value=0) # vytvoříme tabulku s počtem transakcí podle týdne a dne v týdnu
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_sales = weekly_sales.reindex(columns=days_order)
plt.figure(figsize=(12, 8))
sns.heatmap(weekly_sales, cmap='plasma', annot=True, fmt='g', linewidths=.5)
plt.title('Počet transakcí podle týdne a dne v týdnu')
plt.ylabel('Číslo týdne')
plt.yticks(rotation=0)
plt.xlabel('')
plt.show()
