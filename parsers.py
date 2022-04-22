import re
from zipfile import ZipFile
import numpy as np
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.max_colwidth', 100)

def parse_graphml(graphml_str, headers):
    '''
    Parse a graphml file contents to a dataframe
    :param graphml_str (string): The file contents to parse
    :param headers (list): The columns to parse
    '''
    nodes = graphml_str.split('</node>')
    nodes = [s for s in nodes if 'node id' in s]
    nodes = [n.lstrip().rstrip() for n in nodes]
    nodes = [n.replace('"', '') for n in nodes]
    # Exclude file header
    nodes = nodes[1:]

    nodes_df = pd.DataFrame()
    for node in nodes:
        node_rows = node.split('\n')
        id = re.findall('=(.*?)>', node_rows[0])[0]
        node_rows = node_rows[1:]
        keys = ['ID'] + [re.findall('=(.*?)>', n)[0] for n in node_rows]
        values = [id] + [re.findall('>(.*?)<', n)[0] for n in node_rows]
        node_df = pd.DataFrame([values], columns = keys)
        nodes_df = nodes_df.append(node_df)

    return nodes_df[headers]

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

#format_parser = {'graphml': parse_graphml('', []), 'csv': parse_csv('', [])}

def parse_files(raw_files, headers, format):
    '''
    Parse graphml files and join the parsed products to a dataframe
    raw_files(dictionary): Files raw response keyed by the files' cluster_key
    '''
    parsed_dfs = pd.DataFrame()
    for name, file_data in raw_files.items():
        print('name:', name)
        if format == 'graphml': parsed_df = parse_graphml(file_data, headers)
        elif format == 'csv': parsed_df = parse_csv(file_data, headers)
        parsed_dfs = parsed_dfs.append(parsed_df)
    return parsed_dfs

headers = ['ID', 'Label', 'PlannedStart', 'PlannedEnd']

format = 'csv'
zipped_object = ZipFile('./zipped_files/{f}.zip'.format(f=format), "r")
file_names = zipped_object.namelist()
print('zipped file_names:', file_names)
unzipped = {}
for file_name in file_names:
    print(file_name)
    file_posted = zipped_object.read(file_name).decode()
    print(type(file_posted))
    unzipped[file_name] = file_posted

print('unzipped file cluster_key:', unzipped.keys())
parsed_dfs = parse_files(unzipped, headers, format)
print(parsed_dfs.info())
print(parsed_dfs.head())
