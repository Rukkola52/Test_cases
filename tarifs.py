import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path_to_excel = 'C:\\Users\\Kosty\\PycharmProjects\\test_coffee\\calls.xlsx'
df = pd.read_excel(path_to_excel)
df['Дата звонка'] = pd.to_datetime(df['Дата звонка'], dayfirst=True)
df['Дата звонка'] = df['Дата звонка'].dt.date
duration = 'Длительность разговора'
date = 'Дата звонка'
df = df.sort_values([date], axis=0, ascending=True)
df[duration] = pd.to_datetime(df[duration]).dt.ceil('min').dt.strftime('%M').astype(int)


# Первый тариф
first_tarif = pd.DataFrame(df)

par_1 = first_tarif[duration] <= 1
par_2 = first_tarif[duration] <= 10
count_1 = first_tarif[duration] * 1.5
count_2 = (first_tarif[duration] - 1) * 0.5 + 1.5
count_3 = (first_tarif[duration] - 10) * 1 + 1.5 + 9 * 0.5
first_tarif['cost'] = np.where(par_1, count_1, np.where(par_2, count_2, count_3))

first_tarif_cost = first_tarif['cost'].sum()

# Второй тариф
second_tarif = pd.DataFrame(df)

second_tarif = second_tarif.groupby(date).sum().reset_index()
par_1 = second_tarif[duration] <= 5
count_1 = second_tarif[duration] * 3.95
count_2 = (second_tarif[duration] - 5) * 0.4 + 5 * 3.95
second_tarif['cost'] = np.where(par_1, count_1, count_2)
second_tarif_cost = second_tarif['cost'].sum()

# Третий тариф
third_tarif = pd.DataFrame(df)

third_tarif[date] = pd.to_datetime(third_tarif[date])
third_tarif[date] = third_tarif[date].dt.strftime('%Y-%m')
third_tarif = third_tarif.groupby(date).sum().reset_index()

par_1 = third_tarif[duration] <= 555
count_1 = 555
count_2 = (third_tarif[duration] - 555) * 1.95 + 555
third_tarif['cost'] = np.where(par_1, count_1, count_2)
third_tarif_cost = third_tarif['cost'].sum()

# Четвертый тариф
fourth_tarif = pd.DataFrame(df)

par_1 = fourth_tarif[duration] <= 1
count_1 = fourth_tarif[duration] * 1
count_2 = round(((fourth_tarif[duration] - 1) * 0.33 + 1), 4)

fourth_tarif['cost'] = np.where(par_1, count_1, count_2)
fourth_tarif_cost = round((fourth_tarif['cost'].sum()), 2)

# Пятый тариф
fifth_tarif = pd.DataFrame(df)

cond_1 = fifth_tarif[duration] * 0.9
cond_2 = (fifth_tarif[duration] - 5) * 0.05 + 5 * 0.9
cond_3 = fifth_tarif[duration] - 30 + 5 * 0.9 + 25 * 0.05
fifth_tarif['cost'] = np.where((fifth_tarif[duration] <= 5), cond_1,
                               (np.where((fifth_tarif[duration] <= 30), cond_2, cond_3)))
fifth_tarif_cost = fifth_tarif['cost'].sum().round(2)

#Вывод
print('Общая стоимость первого тарифа за 6 мес: ', first_tarif_cost)
print('Общая стоимость второго тарифа за 6 мес: ', second_tarif_cost)
print('Общая стоимость третьего тарифа за 6 мес: ', third_tarif_cost)
print('Общая стоимость четвертого тарифа за 6 мес: ', fourth_tarif_cost)
print('Общая стоимость пятого тарифа за 6 мес: ', fifth_tarif_cost)

lst= [['Билайн Монстр общения', round(first_tarif_cost/6,2)],['Билайн Хочу сказать',round(second_tarif_cost/6)],['Билайн Больше слов',round(third_tarif_cost/6,2)],
['Мегафон 33 копейки',round(fourth_tarif_cost/6,2)],['МТС Много звонков',round(fifth_tarif_cost/6,2)]]
tarifs_cost=pd.DataFrame(lst, columns =['Тариф', 'Средняя стоимость в месяц'])
print(tarifs_cost)
min_tarif=min(tarifs_cost['Средняя стоимость в месяц'])

print('Самый выгодный тариф')
print(tarifs_cost[tarifs_cost['Средняя стоимость в месяц'] == tarifs_cost['Средняя стоимость в месяц'].min()])


# with pd.ExcelWriter('tarifs.xlsx') as writer:
#     first_tarif.to_excel(writer, sheet_name='first_tarif')
#     second_tarif.to_excel(writer, sheet_name='second_tarif')
#     third_tarif.to_excel(writer, sheet_name='third_tarif')
#     fourth_tarif.to_excel(writer, sheet_name='fourth_tarif')
#     fifth_tarif.to_excel(writer, sheet_name='fifth_tarif')


#df.plot(kind='bar', x='Дата звонка', y='Длительность разговора', figsize=(25, 6)).get_figure()
# fig.savefig('test.pdf')
#plt.show()