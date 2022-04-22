import os
import mpxj
import jpype
jpype.startJVM()
from net.sf.mpxj.primavera import PrimaveraXERFileReader
data_dir = '/home/rony/Projects_Code/Cluster_Activities/data/experiments'
files = ['826_As-built_Programme.xer', '820_As-built_Programme_20150501.xer', '823A_As-built_Programme.xer']
file_name = files[0]
xer_file_path = os.path.join(data_dir, file_name)
reader = PrimaveraXERFileReader()
resourceFieldMap = reader.getResourceFieldMap()
wbsFieldMap = reader.getWbsFieldMap()
activityFieldMap = reader.getActivityFieldMap()
assignmentFieldMap = reader.getAssignmentFieldMap()
print(type(activityFieldMap))
print(dict(activityFieldMap))
for k,v in dict(activityFieldMap).items():
	print('{k}:{v}'.format(str(k), v))
jpype.shutdownJVM()