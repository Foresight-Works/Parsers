import os
import re
import pandas as pd
import sys
modules_dir = '/home/rony/Projects_Code/Cluster_Activities/modules'
if modules_dir not in sys.path:
    sys.path.append(modules_dir)
from parsers import *

headers = ['ID', 'TaskType', 'Label', 'PlannedStart', 'PlannedEnd', 'ActualStart', 'ActualEnd', 'Float', 'Status']
files_path = '/home/rony/Projects_Code/Cluster_Activities/data/MTR_Tunnels/xers'
files = os.listdir(files_path)
files_num = ['820', '821', '823A']
files = [f for f in files if any(y in f for y in files_num)]
print(files)
parsed_dfs = pd.DataFrame()
for file in files:
    results_file = '{f}.xlsx'.format(f=file.replace('.xer', ''))
    print(file, results_file)
    file = files[0]
    xer_file_path = os.path.join(files_path, file)
    graphml_file = xer_nodes(xer_file_path)
    graphml_str = open(graphml_file).read()
    parsed_df = parse_graphml(graphml_str, headers)
    #print(parsed_df.info())
    print('{n1} rows | {n2} dedupliated rows'.format(n1=len(parsed_df), n2=len(parsed_df.drop_duplicates())))
    parsed_df.to_excel(results_file, index=False)
    parsed_dfs = pd.concat([parsed_dfs, parsed_df])

parsed_dfs.to_excel('parsed_data.xlsx', index=False)