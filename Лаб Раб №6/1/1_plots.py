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


filename = "1_game_logs.csv"
folder = filename.split(".")[0]
# 9. Используя оптимизированный набор данных, построить пять-семь графиков
# (включая разные типы: линейный, столбчатый, круговая диаграмма, корреляция и т.д.)
need_dtypes = read_types(f"results/{folder}/dtypes.json")
df = pd.read_csv(f"results/{folder}/df_chunks.csv", usecols=lambda x: x in need_dtypes.keys(), dtype=need_dtypes)

# График 1. Гистограмма по дням недели
plt.figure(figsize=(12, 7))
plot = df['day_of_week'].value_counts().plot(kind='bar', title='Частота по дням недели')
plot.figure.savefig(f"results/{folder}/plot1.png")

# График 2. Pairplot по признаку day_of_week
fig = plt.figure(figsize=(15, 15))
sns.pairplot(data=df[["day_of_week", "v_score", "length_minutes", "v_hits"]],
             hue='day_of_week',
             palette='bwr') \
    .savefig(f"results/{folder}/plot2.png")

# График 3. Boxplot по продолжительности
fig = plt.figure(figsize=(12, 7))
sns.boxplot(data=df.query("length_minutes < 1000"),
            x="length_minutes",
            y="day_of_week")
plt.title("Game length and day of week boxplot")
plt.savefig(f"results/{folder}/plot3.png")

# График 4. Heatmap
plt.figure(figsize=(15, 15))
df_copy = df.copy()
df_copy.pop('day_of_week')
df_copy.pop("date")
copy_corr = df_copy.corr()
sns.heatmap(copy_corr, annot=True)
plt.savefig(f"results/{folder}/plot4.png")

# График 5. Kdeplot по признаку length_minutes
fig = plt.figure(figsize=(12, 7))
sns.kdeplot(data=df.query("length_minutes < 400"), x="length_minutes")
plt.title("Game length kdeplot")
plt.savefig(f"results/{folder}/plot5.png")
