import requests
import json

# Configurações do Zabbix
ZABBIX_URL = 'http://xxx.xxx.xxx/zabbix/api_jsonrpc.php'
ZABBIX_USER = 'Admin'
ZABBIX_PASSWORD = 'zabbix'

# Função para realizar requisições à API do Zabbix
def zabbix_request(method, params):
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'auth': token,
        'id': 1
    }
    response = requests.post(ZABBIX_URL, headers=headers, data=json.dumps(data))
    return response.json()

# Autenticação na API
auth_params = {
    'username': ZABBIX_USER,
    'password': ZABBIX_PASSWORD
}
auth_data = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': auth_params,
    'id': 1
}
auth_response = requests.post(ZABBIX_URL, headers={'Content-Type': 'application/json-rpc'},
                              data=json.dumps(auth_data))
token = auth_response.json()['result']

# Nome do host e URL para monitoramento
hosts_urls = [
    {'name': 'google', 'url': 'http://www.google.com'},
    {'name': 'example', 'url': 'http://example.com'},
    {'name': 'globo', 'url': 'www.globo.com'},
    {'name': 'uol', 'url': 'www.uol.com'}
]

# Iterar sobre os hosts e URLs
for item in hosts_urls:
    # Criar o host sem interface e template
    host_params = {
        'host': item['name'],
        'groups': [{'groupid': '2'}]  # ID do grupo onde o host será adicionado
    }
    host_response = zabbix_request('host.create', host_params)
    host_id = host_response['result']['hostids'][0]

    # Criar monitoramento web
    http_test_params = {
        'name': item['name'],
        'hostid': host_id,
        'delay': '5m',
        'agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'steps': [{
            'name': item ['name'],
            'url': item['url'],
            'status_codes': '200-499',
           'no': 1
        }]
    }

    http_test_response = zabbix_request('httptest.create', http_test_params)
    http_test_id = http_test_response['result']['httptestids'][0]

    # Criar trigger
    trigger_params = {
        'description': f"{item['name']} url indisponível",
        'expression': f"last(/{item['name']}/web.test.rspcode[{item['name']},{item['name']}])>499",
        #'expression': f"last(/{host_name}/web.test.rspcode[Meu Web Monitor,Verificar URL])>499",
        'priority': 4  # High
        'tags': [
            {
                'tag': 'sla',
                'value': f"{item['name']}"
            }
        ]
    }
    trigger_response = zabbix_request('trigger.create', trigger_params)

    if 'result' in trigger_response:
        print(f"Trigger criada com sucesso para '{item['name']}': {trigger_response['result']['triggerids'][0]}")
    else:
        print(f"Erro ao criar trigger para '{item['name']}':", trigger_response)

    print(f"Host criado com ID: {host_id} e Nome: {item['name']}")
    print(f"Monitoramento Web criado com ID: {http_test_id}")
    print()
