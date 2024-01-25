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


filename = "2_automotive.csv.zip"
folder = filename.split(".")[0]
# 9. Используя оптимизированный набор данных, построить пять-семь графиков
# (включая разные типы: линейный, столбчатый, круговая диаграмма, корреляция и т.д.)
need_dtypes = read_types(f"results/{folder}/dtypes.json")
df = pd.read_csv(f"results/{folder}/df_chunks.csv", usecols=lambda x: x in need_dtypes.keys(), dtype=need_dtypes)

# График 1. Частота по типу трансмиссии
plt.figure(figsize=(12, 7))
plot = df['vf_TransmissionStyle'].value_counts().plot(kind='bar', title='Частота по типу трансмиссии')
plot.figure.savefig(f"results/{folder}/plot1.png")

# График 2. Pairplot по признаку isNew
fig = plt.figure(figsize=(15, 15))
sns.pairplot(data=df[["isNew", "vf_BasePrice", "vf_DisplacementCC", "vf_EngineHP"]],
             hue='isNew',
             palette='bwr') \
    .savefig(f"results/{folder}/plot2.png")

# График 3. Boxplot по askPrice
fig = plt.figure(figsize=(12, 7))
sns.boxplot(data=df.query("askPrice < 100000"),
            x="askPrice",
            hue="isNew",
            orient="vertical")
plt.title("AskPrice boxplot")
plt.savefig(f"results/{folder}/plot3.png")

# График 4. Heatmap
plt.figure(figsize=(15, 15))
sns.heatmap(df.drop(["isNew", "vf_TransmissionStyle"], axis=1).corr(), annot=True)
plt.savefig(f"results/{folder}/plot4.png")

# График 5. Kdeplot по признаку vf_BasePrice
fig = plt.figure(figsize=(12, 7))
sns.kdeplot(data=df.query("vf_BasePrice < 125000"), x="vf_BasePrice")
plt.title("Game length kdeplot")
plt.savefig(f"results/{folder}/plot5.png")
