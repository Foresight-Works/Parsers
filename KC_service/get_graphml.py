import requests
file_url = 'http://172.31.25.89:8080/v1.0/api/bo/getGraphMLFile?id=-687733302'
response = requests.get(file_url)
print(response)
print(response.text)
