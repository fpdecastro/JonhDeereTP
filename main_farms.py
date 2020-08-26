import requests
from requests_oauthlib import OAuth1
import pyodbc

headers = {
    'Accept' : 'application/vnd.deere.axiom.v3+json'
}

CONSUMER_KEY = 'johndeere-JcFsHU6CV0klrsgkDHewTLuSAP1QZ2Q8Tx9sFCOs' 
CONSUMER_SECRET = '5b67d63b58a9e80facb93354b18a79eb9be3b668f02e331cace8f5a4190254fa'
TOKEN = 'd8d3c1b7-8f56-4cc3-96a6-0b6da898eea6'
TOKEN_SECRET = '19Ryi+uXOFxS3/8Q0h+pHjlGVXaYndLhTOl64Wg4cdA4/5ly0f48DxcN+nBsfFgXP71ruvCHMb4T5fYXeGzQ5uAzGYDKyfONgE0Mp6y1bbA='

# Defino el servidor y la base de datos
server = 'DESKTOP-FP2QGMT\MSSQL2014' 
database = 'JohnDeere'

if __name__ == "__main__":
    # Me conecto a la base de datos
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +'; DATABASE='+ database +'; Trusted_Connection=yes;')
    
    #Creo la connection al cursor
    cursor = cnxn.cursor()
    
    #Definimos le script en SQL
    sql_query = ''' INSERT INTO farms(id_farm, name, id_client)
                     VALUES (?, ?, ?)'''

    url= 'https://sandboxapi.deere.com/platform/organizations'
    AUTH = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)
    
    response = requests.get(url, headers=headers ,auth=AUTH)
    # Recibo el request y lo transformo a json()
    response_json = response.json()
    # Recibo un diccionario y necesito values
    response_values = response_json['values']
    # itero para ver los nombres

    for organizations in response_values:
        id_organizations = organizations['id']
        
        url_new = url + '/' + id_organizations + '/clients'
        response_client = requests.get(url_new, headers=headers, auth=AUTH)
        
        response_client_json = response_client.json()
        response_clients_value = response_client_json['values']
        
        for client in response_clients_value:
            
            client_id = client['id']    
            url_newest = url_new +'/' + client_id + '/farms'
            response_farm = requests.get(url_newest, headers=headers, auth=AUTH).json()
            response_farm_value = response_farm['values']
            
            for farm in response_farm_value:
                farm_id = farm['id']
                farm_name = farm['name']
                print(farm_id,' -------> ', farm_name,' -------> ', client_id)
        
                insert_values = (farm_id, farm_name, client_id)
                cursor.execute(sql_query, insert_values)
    
    cnxn.commit()
    
    cursor.close()
    