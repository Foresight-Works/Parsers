import pandas as pd
import os
import jpype
import mpxj
dir = '/home/rony/Projects_Code/Cluster_Activities/data/MTR_Tunnels/xers'
files = os.listdir(dir)
file = files[0]
print('Data:', file)
path = os.path.join(dir, file)

jpype.startJVM()
from net.sf.mpxj.reader import UniversalProjectReader
project = UniversalProjectReader().read(path)

'''
Node representation example:
<node id="A3920">
    <data key="Label">ENVIRONMENTAL PERMIT ISSUED</data>
    <data key="TaskType">TT_Mile</data>
    <data key="PlannedStart">28/06/2021</data>
    <data key="PlannedEnd">28/06/2021</data>
    <data key="ActualStart">14/06/2016</data>
    <data key="ActualEnd">14/06/2016</data>
    <data key="Float">0</data>
    <data key="Status">TK_Complete</data>
'''
tasks = project.getTasks()
for task in project.getTasks():
	task_features, task_lines = {}, []
	task_features["id"] = task.getID()
	task_features["TaskType"] = task.getActivityType()
	task_features["Label"] = task.getName()
	task_features["PlannedStart"] = task.getPlannedStart()
	task_features["PlannedEnd"] = task.getPlannedFinish() # ?task.getPlannedFinish
	task_features["ActualStart"] = task.getActualStart()
	task_features["ActualEnd"] = task.getActualFinish()
	if task.getFreeSlack():
		task_features["Float"] = task.getFreeSlack().getDuration()
	else: task_features["Float"] = None
	task_features["Status"] = task.getActivityStatus()
	print('task features:', list(task_features.keys()))
	for feature, object in task_features.items():
		try:
			if object: object_str = object.toString()
			else: object_str = ''
		except AttributeError as e:
			object_str = str(object)
		if feature == 'id':
			line = '<node id="{o}">'.format(o=object_str)
		else:
			line = '<data key="{f}">{o}</data>'.format(f=feature, o=object_str)
		task_lines.append(line)
	print('task lines')
	task_lines = '\n'.join(task_lines)
	print(task_lines)

jpype.shutdownJVM()

