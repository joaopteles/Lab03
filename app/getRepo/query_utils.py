import requests
import time


def criar_query(params, query_template):
    q = query_template
    for k in params.keys():
        value = params[k]
        if type(value) == int:
            q = q.replace(k, '%d' % value)
        else:
            q = q.replace(k, "null") if value == "" else q.replace(
                k, '"%s"' % value)
    return q


def execute_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers={
        'Content-Type': 'application/json',
        'Authorization': 'bearer API_KEY'
    })
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 502:
        return execute_query(query)
