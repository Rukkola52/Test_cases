import pandas as pd
import numpy as np

path_to_csv='Транзакции.csv'
df = pd.read_csv(path_to_csv, delimiter='\t', encoding='ANSI', decimal=",")

df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m')
df = df[df['Доставка'] == 0]
transaction_count = df.shape[0]
df['paid_with_promo'] = np.where(df['Promo'] == 1,df['Paid'],0)
df['cost_with_promo'] = np.where(df['Promo'] == 1,df['Cost'],0)
df['paid_without_promo'] = np.where(df['Promo'] != 1,df['Paid'],0)
df['cost_without_promo'] = np.where(df['Promo'] != 1,df['Cost'],0)

group_df = df.groupby('Date').sum().reset_index() # DF
group_df['monthly_transaction_count'] = df.groupby('Date').count().reset_index()['Count']

output_df= pd.DataFrame({'Месяц' : group_df['Date'],
                  'Введен промокод' : group_df['Promo'],
                  'Кол-во транзакций' : group_df['monthly_transaction_count'],
                  'Плохих отзывов, %' : group_df['Плохой отзыв']/group_df['monthly_transaction_count']*100,
                  'Доходность с промокодом, %' : (group_df['paid_with_promo'] - group_df['cost_with_promo'])/group_df['cost_with_promo']*100,
                  'Доходность без промокода, %' : (group_df['paid_without_promo'] - group_df['cost_without_promo'])/group_df['cost_without_promo']*100,
                  'Доходность средняя, %' : (group_df['Paid'] - group_df['Cost'])/group_df['Cost']*100})

print(output_df)

output_df.to_excel("transactions.xlsx")