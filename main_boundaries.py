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

def request_test(url, head, verification):
    # Hago un request hacerca de la petición
    response = requests.get(url, headers=head, auth=verification)
    while response.status_code != 200:
        print(response.status_code)
        response = requests.get(url, headers=head, auth=verification)
    return response.json()
    


if __name__ == "__main__":
    # Me conecto a la base de datos
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +'; DATABASE='+ database +'; Trusted_Connection=yes;')
    
    #Creo la connection al cursor
    cursor = cnxn.cursor()
    
    #Definimos le script en SQL
    sql_query = ''' INSERT INTO boundaries(boundaries_name, sourceType, createdTime, modifiedTime, archived, id_boundaries, active, irrigated, id_field)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''

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
        response_client_json = requests.get(url_new, headers=headers, auth=AUTH).json()
        
        response_clients_value = response_client_json['values']
        
        for client in response_clients_value:

            client_id = client['id']    
            url_newest = url_new +'/' + client_id + '/farms'
            response_farm = requests.get(url_newest, headers=headers, auth=AUTH).json()
            response_farm_value = response_farm['values']
            
            for farm in response_farm_value:
                farm_id = farm['id']
                url_newest_field = url + '/' + id_organizations + '/farms/' + farm_id + '/fields'
                response_field = requests.get(url_newest_field, headers=headers, auth=AUTH).json()
                response_field = response_field['values']

                for field in response_field:

                    field_id = field['id']
                    url_newest_boundaries = url + '/' + id_organizations + '/fields/' + field_id + '/boundaries' 
                    # response_boundaries = requests.get(url_newest_boundaries, headers=headers, auth=AUTH)
                    response_boundaries_json = request_test(url_newest_boundaries, headers, AUTH)
                    # print(response_boundaries_json)
                    response_boundaries_value = response_boundaries_json['values']
                    
                    if response_boundaries_value != []:
                        for boundaries in response_boundaries_value:
                            boundaries_name = boundaries['name']
                            sourceType = boundaries['sourceType']
                            createdTime = boundaries['createdTime']
                            modifiedTime = boundaries['modifiedTime']
                            archived = boundaries['archived']
                            id_boundaries =boundaries['id']
                            active = boundaries['active']
                            irrigated = boundaries['irrigated']
                            print(boundaries_name, sourceType, createdTime, modifiedTime, archived, id_boundaries, active, irrigated)
                            insert_values = (boundaries_name, sourceType, createdTime, modifiedTime, archived, id_boundaries, active, irrigated, field_id)
                            cursor.execute(sql_query, insert_values)    
    cnxn.commit()
    
    cursor.close()

    

    
    


