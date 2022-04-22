import os
import mpxj
import jpype
jpype.startJVM()
from net.sf.mpxj.reader import UniversalProjectReader
from net.sf.mpxj.primavera import PrimaveraXERFileReader
from net.sf.mpxj import ActivityStatus
from net.sf.mpxj import ActivityType

data_dir = '/home/rony/Projects_Code/Cluster_Activities/data/experiments'
files = ['826_As-built_Programme.xer', '820_As-built_Programme_20150501.xer', '823A_As-built_Programme.xer']
headers = ['ID', 'TaskType', 'Label', 'PlannedStart', 'PlannedEnd', 'ActualStart', 'ActualEnd', 'Float', 'Status']
file_name = files[0]
xer_file_path = os.path.join(data_dir, file_name)
print('xer_file_path:\n', xer_file_path)
reader = UniversalProjectReader()
project = reader.read(xer_file_path)
#resources = project.getAllResources()
#for resource in resources: print(resource)
# AttributeError: 'net.sf.mpxj.ProjectFile' object has no attribute 'getAllResources'


jpype.shutdownJVM()
