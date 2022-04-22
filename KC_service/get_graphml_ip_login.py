import requests
API_ENDPOINT = "http://172.31.47.85:8080/v1.0/admin/bo/login"
data = \{ "password": "Test12345$", "username": "ms-test@foresight.works"}
response = requests.post(url = API_ENDPOINT,  json = data )
print(response.status_code)
r_joson=response.json()
access_token=r_joson\['accessToken']
print(access_token)
API_ENDPOINT = "http://172.31.47.85:8080/v1.0/api/bo/getStoredXerFileVersions?contractId=-1&projectId=3"
my_headers = \{"Authorization" : "Bearer " + access_token}
response = requests.get(API_ENDPOINT, headers=my_headers)
print(response.status_code)
r_joson=response.json()
print(r_joson)