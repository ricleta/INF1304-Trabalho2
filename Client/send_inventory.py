import requests
import json

func_url = "https://6iim4chjw4dp7omphd2xf6tdtm0yspcz.lambda-url.us-east-1.on.aws/"

produtos =[ 
    {
        'store': 'Rio de Janeiro',
        'item': 'Hats',
        'count': 5
    },
    
    {
        'store': 'Rio de Janeiro',
        'item': 'Guns',
        'count': 100
    },

    {
        'store': 'Rio de Janeiro',
        'item': 'Books',
        'count': 0
    },
]

dados = json.dumps(produtos)

header = {
    'Content-Type': 'application/json',
}
response = requests.post(func_url, data=dados, headers=header)