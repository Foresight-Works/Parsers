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
	tasks_rows = []
	for task in tasks:
		if task.getFreeSlack():
			task_float = task.getFreeSlack().getDuration()
		else: task_float = None
		task_row = [task.getID(), task.getActivityType(), task.getName(),\
					task.getPlannedStart(), task.getPlannedFinish(),\
					task.getActualStart(), task.getActualFinish(), task_float, task.getActivityStatus()]
		tasks_rows.append(task_row)
	return pd.DataFrame(tasks_rows, columns=headers)
	jpype.shutdownJVM()

print('xer_file_path:', xer_file_path)
tasks_df = xer_nodes(xer_file_path)
print(tasks_df)
tasks_df.to_excel('tasks_df.xlsx', index=False)




