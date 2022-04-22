import os
import pandas as pd
import re

def data_to_table(table_columns, table_data):
    return pd.DataFrame(data=table_data, columns=table_columns)
def read_xer(xer_file):
    line_types = ['%T', '%F', '%R', '%E']
    tables = dict()
    with open(xer_file, 'r', encoding='latin1') as xer:
        table_name, table_columns, table_data = None, [], []
        for line in xer:
            split_line = re.split("\t", line.replace('\n', ''))
            # skip lines not starting with a valid line type
            # (eg file info stuff)
            if split_line[0] not in line_types:
                continue
            # %T = table
            if split_line[0] == '%T':
                if table_name is not None:
                    try:
                        tables[table_name] = data_to_table(table_columns,
                                                           table_data)
                    except:
                        pass
                table_name = split_line[1]
                table_columns, table_data = [], []
            # %F = fields
            if split_line[0] == '%F':
                table_columns = split_line[1:]
            # %R = record
            # ERRORS WITH SOME TABLES?
            if split_line[0] == '%R':
                table_data.append(split_line[1:])
            # %E = end
            if split_line[0] == '%E' and table_name is not None:
                try:
                    tables[table_name] = data_to_table(table_columns,
                                                                   table_data)
                except:
                    pass
    return tables

dir = '/home/rony/Projects_Code/Cluster_Activities/data/MTR_Tunnels/xers'
files = os.listdir(dir)
file = '823A_As-built_Programme.xer'
#for file in files:
path = os.path.join(dir, file)
print('path:', path)
tables = read_xer(path)

print(tables.keys())
q = 'Construction Stage Mobile Phone Network'
for name, table in tables.items():
    if 'task_name' in table.columns:
        print(60*'+')
        print(name)
        results_file = '{f}.xlsx'.format(f=file.replace('.xer', ''))
        table.to_excel(results_file, index=False)
    #     tasks = list(table['task_name'])
    #     #print('tasks:', tasks)
    #     f = [t for t in tasks if q in t]
    #     print(f)
    #     tasks.sort()
    #     for t in tasks: print(t)
        #print(table)
        #print(table.columns)
        #table['task_id'] = table['task_id'].astype(int)
        #print(table['task_id'].describe())
        # for c in table.columns:
        #     print(c)
        #     cvals = list(table[c])
        #     f = [v for v in cvals if q in v]
        #     #print(table[c].head())
        #     print(f)