'''3. Otázka.
Která kategorie se prodává nejčastěji spolu s produkty z kategorie Televize (resp. jsou spolu v jedné objednávce)?
'''
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.ExcelFile('Data.xlsx') # načteme excel soubor
df_transactions = data.parse('Transactions') # načte list Transactions
df_products = data.parse('Products') # načte list Products
df_merged = pd.merge(df_transactions, df_products, on='Product name', how='inner') #sloučí listy podle názvu produktu

televize_transactions = df_merged[df_merged['Category'] == 'Televize'] # vybereme transakce s Televizemi

# Určujeme kategorie produktů, které se nejčastěji prodávají společně s 'Televize'
with_tv = df_merged[df_merged['Transaction ID'].isin(televize_transactions['Transaction ID'])]

# Počítáme počet prodejů pro každou kategorii, která se prodává společně s 'Televize'.
category_counts = with_tv['Category'].value_counts().reset_index()

# Vytiskneme výsledky
print("Kategorie produktů, které se prodávají nejčastěji spolu s produkty z kategorie 'Televize':")
print(category_counts)

with_tv = with_tv.groupby(['Category', 'Transaction ID']).size().unstack(fill_value=0)

# Děláme tepelnou mapu
plt.figure(figsize=(12, 8))
sns.heatmap(with_tv, cmap='Purples', annot=True, fmt='g', linewidths=.5)
# Nastavíme popisky
plt.title('Počet kategorií prodavaných spolu s Televize')
plt.xlabel('Transaction ID')
plt.ylabel('')
plt.yticks(rotation=0)
plt.xticks(rotation=0)
plt.show()
