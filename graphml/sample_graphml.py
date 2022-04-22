import pandas as pd
import numpy as np
import random
import re
pd.set_option("display.max_rows", None,\
              "display.max_columns", None, 'display.max_colwidth', 100)


def sample_graphml(graphml_str, smaple_size):
    '''
    Parse a graphml file contents to a dataframe
    :param graphml_str (string): The file contents to parse
    :param smaple_size(int): The number of nodes to extract
    '''
    nodes = graphml_str.split('</node>')[1:]
    nodes = [s for s in nodes if 'node id' in s]
    nodes = ['</node>'+s for s in nodes]
    #nodes = [n.lstrip().rstrip() for n in nodes]
    #nodes = [n.replace('"', '') for n in nodes]
    indices = list(np.arange(len(nodes)))
    print(indices)
    sample_indices = random.sample(indices, smaple_size)
    nodes = np.array(nodes)
    sample = list(nodes[sample_indices])
    return sample

file = 'CCGTD1_IPS.graphml'
graphml_str = open(file).read()
sample_fn = '{f}_sample.graphml'.format(f=file.split('.')[0])
sample = sample_graphml(graphml_str, 100)
print('{n} nodes sampled'.format(n=len(sample)))
with open(sample_fn, 'w') as f:
    for n in sample:
        f.write('{n}\n'.format(n=n))