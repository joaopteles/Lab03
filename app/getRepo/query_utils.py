import requests
import time


def criar_query(params, query_template):
  q = query_template
  for k in params.keys():
      value = params[k]
      if type(value) == int:
          q = query.replace(name, '%d' % value)
      else:
          q = query.replace(name, "null") if value == "" else query.replace(name, '"%s"' % value)
  return q

def execute_query(query):
    try:
        request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = {
        'Content-Type': 'application/json',
        'Authorization': 'bearer '
        })

    if  request.status_code == 200:
        return request.json()
    elif request.status_code == 502:
        return execute_query(query)

