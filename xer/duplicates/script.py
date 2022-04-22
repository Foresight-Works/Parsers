import pandas as pd
import os
import re

dir = '/home/rony/Projects_Code/Cluster_Activities/data/MTR_Tunnels/xers'
files = os.listdir(dir)
for file in files:
    path = os.path.join(dir, file)
    file_tables = open(path).read().split('%T')
    for table in file_tables:
        table_lines = table.split('\n')
        headers_line = [l for l in table_lines if re.findall('^%F',l)]

        print(60 * '=')
        print(table_lines[0])
        print(headers_line)
