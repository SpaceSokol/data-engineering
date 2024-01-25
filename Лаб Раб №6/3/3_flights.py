import pandas as pd
import utils

import warnings
warnings.filterwarnings("ignore")

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

filename = "3_flights.csv"
full_filename = f"data/{filename}"
res_folder = f"results/{filename.split('.')[0]}/"

# 1. Загрузить набор данных из файла
df = utils.read_file(full_filename)

#2.	Провести анализ набора данных по следующим параметрам:
    #a.	Объем памяти, который занимает файл на диске
    #b.	Объем памяти, который занимает набор данных при загрузке в память
    #c.	Вычислить для каждой колонки занимаемый объем памяти, долю от общего объема, а также выяснить тип данных
#3.	Полученный набор данных отсортировать по занимаемому объему памяти
# Вывести в файл (json) данные по колонкам с пометкой, что это статистика по набору данных без применения оптимизаций.
output_file = res_folder + "file_size.json"
utils.analyze_file_size(df, full_filename, output_file)

#4.	Преобразовать все колонки с типом данных «object» в категориальные, если количество уникальных значений колонки составляет менее 50%.
#5.	Провести понижающее преобразование типов «int» колонок
#6.	Провести понижающее преобразование типов «float» колонок
optimized_dataset = df.copy()

converted_obj = utils.optimize_obj(df)
converted_int = utils.optimize_int(df)
converted_float = utils.optimize_float(df)

# 7. Повторно провести анализ набора данных, как в п. 2, сравнив показатели занимаемой памяти
optimized_dataset[converted_obj.columns] = converted_obj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

output_file_opt = res_folder + "file_size_opt.json"
utils.analyze_file_size(optimized_dataset, full_filename, output_file_opt)

#8.	Выбрать произвольно 10 колонок для дальнейшем работы, прописав преобразование типов и загрузку только нужных данных на этапе чтения файла.
# При этом стоит использовать чанки. Сохраните полученный поднабор в отдельном файле.

need_column = dict()
opt_dtypes = optimized_dataset.dtypes

column_names = ['DAY_OF_WEEK', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME',
                'AIRLINE', 'YEAR', 'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'TAIL_NUMBER']
for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f" {key}: {opt_dtypes [key]}")

has_header = True
output_file_chunks = res_folder + "df_chunks.csv"
for chunk in pd.read_csv(full_filename, usecols=lambda x: x in column_names, dtype=need_column, chunksize=100_000):
    print(utils.mem_usage(chunk))
    chunk.to_csv(output_file_chunks, mode="a", header=has_header)
    has_header = False

dtype_json = need_column.copy()
output_file_dtypes = res_folder + "dtypes.json"
for key in dtype_json.keys():
    dtype_json[key] = str(dtype_json[key])
utils.write_to_json(output_file_dtypes, dtype_json)
