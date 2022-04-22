import pandas as pd
import os
import re

def xer_nodes(xer_file_path):
	file = os.path.basename(xer_file_path)
	graphml_file = file.replace('.xer', '.graphml')
	import jpype
	import mpxj
	jpype.startJVM()
	from net.sf.mpxj.reader import UniversalProjectReader
	from net.sf.mpxj import ActivityStatus
	from net.sf.mpxj import ActivityType

	project = UniversalProjectReader().read(xer_file_path)
	tasks = project.getTasks()
	task_features = {}
	for task in tasks:
		task_features, task_lines = {}, []
		task_features["id"] = task.getID()
		task_features["TaskType"] = str(task.getActivityType()).replace('TASK_DEPENDENT', 'TT_TASK')
		task_features["Label"] = task.getName()
		task_features["PlannedStart"] = task.getPlannedStart()
		task_features["PlannedEnd"] = task.getPlannedFinish()
		task_features["ActualStart"] = task.getActualStart()
		task_features["ActualEnd"] = task.getActualFinish()
		if task.getFreeSlack():
			task_features["Float"] = task.getFreeSlack().getDuration()
		else:
			task_features["Float"] = None

		task_features["Status"] = task.getActivityStatus()
		print('task features:', list(task_features.keys()))
		for feature, object in task_features.items():
			try:
				if object:
					object_str = object.toString()
				else:
					object_str = ''
			except AttributeError as e:
				object_str = str(object)
			if feature == 'id':
				line = '<node id="{o}">'.format(o=object_str)
			else:
				line = '<data key="{f}">{o}</data>'.format(f=feature, o=object_str)
			task_lines.append(line)
		print('task lines')
		task_lines = '</node>'+'\n'+'\n'.join(task_lines)+'\n'
		print(task_lines)
		with open(graphml_file, 'a') as f: f.write(task_lines)

	return graphml_file
	jpype.shutdownJVM()

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

data_dir = '/home/rony/Projects_Code/Cluster_Activities/data/experiments'
files = ['826_As-built_Programme.xer', '820_As-built_Programme_20150501.xer', '823A_As-built_Programme.xer']
headers = ['ID', 'TaskType', 'Label', 'PlannedStart', 'PlannedEnd', 'ActualStart', 'ActualEnd', 'Float', 'Status']

file_name = files[0]
xer_file_path = os.path.join(data_dir, file_name)
print('xer_file_path:\n', xer_file_path)
graphml_file = xer_nodes(xer_file_path)
graphml_str = open(graphml_file).read()
headers = ['ID', 'TaskType', 'Label', 'PlannedStart', 'PlannedEnd']
nodes_df = parse_graphml(graphml_str, headers)
print(nodes_df.head())
print(nodes_df.info())
nodes_df.to_excel('nodes_df.xlsx', index=False)

#projects = projects[projects[task_type] == 'TT_Task']

