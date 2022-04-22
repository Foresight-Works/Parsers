import numpy as np
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.max_colwidth', 100)

def parse_csv(csv_string, headers):
    '''
    Parse a csv file contents to a dataframe
    :param csv_string (string): The file contents to parse
    :param headers (list): The columns to parse
    '''
    print('headers to parse:', headers)
    lines = csv_string.split('\n')
    source_headers = lines[0].split(',')
    print('source_headers:', source_headers)
    indices = [source_headers.index(h) for h in headers]
    print('headers indices:', indices)
    lines = [l for l in lines[1:] if l]
    rows = []
    for index, line in enumerate(lines):
        line_array = np.array(line.split(','))
        parsed_values = list(line_array[indices])
        rows.append(parsed_values)
    return pd.DataFrame(rows, columns=headers)

headers = ['ID', 'Label', 'PlannedStart', 'PlannedEnd']
data_str = open('SIME_DARBY_TASKS.csv', encoding='utf-8-sig').read()
parsed_df = parse_csv(data_str, headers)
print(parsed_df.head())

