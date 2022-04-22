import pandas as pd
import os
import jpype
import mpxj
dir = '/data/MTR_Tunnels/xers'
files = os.listdir(dir)
file = files[0]
print('Data:', file)
xer_file_path = os.path.join(dir, file)

jpype.startJVM()
def xer_nodes(xer_file_path):
	from net.sf.mpxj.reader import UniversalProjectReader
	headers = ['ID', 'TaskType', 'Label', 'PlannedStart', 'PlannedEnd', 'ActualStart', 'ActualEnd', 'Float', 'Status']
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
tasks_df = xer_nodes(xer_file_path)
print(tasks_df)
tasks_df.to_excel('tasks_df.xlsx', index=False)
jpype.shutdownJVM()



