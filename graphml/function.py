import pandas as pd
import re
pd.set_option("display.max_rows", None,\
              "display.max_columns", None, 'display.max_colwidth', 100)


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

graphml_str = open('CCGTD1_IPS.graphml').read()
headers = ['ID', 'Label', 'PlannedStart', 'PlannedEnd']
nodes_df = parse_graphml(graphml_str, headers)
print(nodes_df.head())
print(nodes_df.info())