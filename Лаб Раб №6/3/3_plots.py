import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json

pd.set_option("display.max_rows", 20, "display.max_columns", 60)


def read_types(file_name):
    with open(file_name, mode="r") as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] != 'category':
            dtypes[key] = np.dtype(dtypes[key])

    return dtypes


filename = "3_flights.csv"
folder = filename.split(".")[0]
# 9. Используя оптимизированный набор данных, построить пять-семь графиков
# (включая разные типы: линейный, столбчатый, круговая диаграмма, корреляция и т.д.)
need_dtypes = read_types(f"results/{folder}/dtypes.json")
df = pd.read_csv(f"results/{folder}/df_chunks.csv", usecols=lambda x: x in need_dtypes.keys(), dtype=need_dtypes)

# График 1. Частота по дню недели
# plt.figure(figsize=(12, 7))
# plot = df['DAY_OF_WEEK'].value_counts().plot(kind='bar', title='Частота по дню недели')
# plot.figure.savefig(f"results/{folder}/plot1.png")

# График 2. Гистограмма по авиакомпаниям
# fig = plt.figure(figsize=(15, 15))
# plot = df['AIRLINE'].value_counts().plot(kind='bar', title='Гистограмма по авиакомпаниям')
# plot.figure.savefig(f"results/{folder}/plot2.png")

# График 3. График задержки вылета
plt.figure(figsize=(15, 15))
dataset = df.assign(DEPARTURE_DELAY=lambda x: x.DEPARTURE_TIME - x.SCHEDULED_DEPARTURE).loc[
    lambda x: x.DEPARTURE_DELAY >= 1]
gr_obj = dataset.groupby(["DAY_OF_WEEK"])['DEPARTURE_DELAY'].mean()
plt.plot(gr_obj.index, gr_obj.values, color='green')
plt.xticks(range(1, 7))
plt.title("Задержки вылета в зависимости от дня недели")
plt.savefig(f"results/{folder}/plot3.png")

# График 4. Heatmap
# plt.figure(figsize=(15, 15))
# copy = df.copy(deep=True)
# copy.pop('TAIL_NUMBER')
# copy.pop("AIRLINE")
# copy.pop("DESTINATION_AIRPORT")
# copy.pop("ORIGIN_AIRPORT")
# copy_corr = copy.corr()
# sns.heatmap(copy_corr, annot=True)
# plt.title("Корреляция числовых данных")
# plt.savefig(f"results/{folder}/plot4.png")

# График 5. Pairplot
# fig = plt.figure(figsize=(15, 15))
# sns.pairplot(data=dataset,
#              hue='AIRLINE',
#              palette='bwr', ).savefig(f"results/{folder}/plot5.png")
