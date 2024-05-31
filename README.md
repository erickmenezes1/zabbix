# Zabbix Web Monitoring Script

Este script Python automatiza a criação de hosts e a configuração de monitoramento web no Zabbix. Ele permite monitorar URLs específicas a cada 5 minutos usando um agente do Chrome para Linux.

## Requisitos

- Python 3.x
- Bibliotecas `requests` e `json`
- Zabbix configurado e acessível via API

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/erickmenezes1/zabbix
   cd zabbix
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install requests
   ```

## Configuração

Edite o script para configurar as variáveis de acordo com o seu ambiente Zabbix:

- `ZABBIX_URL`: URL do servidor Zabbix.
- `ZABBIX_USER`: Usuário para autenticação na API do Zabbix.
- `ZABBIX_PASSWORD`: Senha para autenticação na API do Zabbix.
- `hosts_urls`: Lista de dicionários contendo o nome do host e a URL para monitoramento.

## Uso

Execute o script:

```bash
python zabbix-multiple-hosts-web.py
```

O script realizará as seguintes etapas para cada host e URL especificados:

1. Autenticação na API do Zabbix.
2. Criação de um novo host.
3. Configuração do monitoramento web para a URL especificada.
4. Criação de um trigger para alertar caso a URL retorne um código de status HTTP superior a 499.
