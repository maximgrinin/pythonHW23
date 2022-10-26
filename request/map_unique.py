import requests

url = "http://127.0.0.1:5000/perform_query"

payload={
  'file_name': 'apache_logs.txt',
  'cmd1': 'map',
  'value1': '0',
  'cmd2': 'unique',
  'value2': ''
}

response = requests.request("POST", url, data=payload)
print(response.text)
