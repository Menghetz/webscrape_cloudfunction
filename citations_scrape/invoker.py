import requests

# http  unauthenticated  endpoint to call
url = "http://localhost:8080"

# the input json payload
param = {"hello":"saed"}

# post your response
r = requests.post(url, json=param)

# print results
print(r.content)