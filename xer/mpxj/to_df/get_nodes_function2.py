import pandas as pd
import os

dir = '/data/MTR_Tunnels/xers'
files = os.listdir(dir)
file = files[0]
print('File name:', file)
xer_file_path = os.path.join(dir, file)
xer_file_path = '/data/experiments/820_As-built_Programme_20150501.xer'
xer_file_path = '/data/MTR_Tunnels/xers/823A_As-built_Programme.xer'
headers = ['ID', 'TaskType', 'Label', 'PlannedStart', 'PlannedEnd', 'ActualStart', 'ActualEnd', 'Float', 'Status']
def xer_nodes(xer_file_path):
	import jpype
	import mpxj
	jpype.startJVM()
	from net.sf.mpxj.reader import UniversalProjectReader
	project = UniversalProjectReader().read(xer_file_path)
	tasks = project.getTasks()
	tasks_features = []
	for task in tasks:
		if task.getFreeSlack():
			task_float = task.getFreeSlack().getDuration()
		else: task_float = None
		task_features = [task.getID(), task.getActivityType(), task.getName(),\
					task.getPlannedStart(), task.getPlannedFinish(),\
					task.getActualStart(), task.getActualFinish(),\
                         task_float, task.getActivityStatus()]
		task_features_str = []
		for feature in task_features:
			try:
				if feature:
					feature_str = feature.toString()
				else:
					feature_str = ''
			except AttributeError:
				feature_str = str(feature)
			task_features_str.append(feature_str)
		tasks_features.append(task_features_str)
	return pd.DataFrame(tasks_features, columns=headers)
	jpype.shutdownJVM()

print('xer_file_path:', xer_file_path)
tasks_df = xer_nodes(xer_file_path)
tasks_df.to_excel('tasks_df.xlsx', index=False)
for col in tasks_df.columns:
	print(col)
	print(tasks_df[col].head())



