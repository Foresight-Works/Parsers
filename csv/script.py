import numpy as np
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.max_colwidth', 100)


data_str = open('SIME_DARBY_TASKS.csv', encoding='utf-8-sig').read()
print(type(data_str))
lines = data_str.split('\n')
headers = lines[0].split(',')
print('headers:', headers)
parsed_headers = ['ID', 'Label', 'PlannedStart', 'PlannedEnd']
indices = [headers.index(h) for h in parsed_headers]
print('parsed_headers_indices:', indices)
lines = [l for l in lines[1:] if l]
results = []
for index, line in enumerate(lines):
    line_array = np.array(line.split(','))
    parsed_values = list(line_array[indices])
    results.append(parsed_values)

parsed_df = pd.DataFrame(results, columns=parsed_headers)
print(parsed_df.head(10))

