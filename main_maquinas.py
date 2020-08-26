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
    sql_query = ''' INSERT INTO machines( visualizationCategory, productKey, engineSerialNumber, telematicsState, guid_machine, modelYear, id_machine, vin, name_machine, id_org)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

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
        url_new = url + '/' + id_organizations + '/machines'
        response_machine = requests.get(url_new, headers=headers, auth=AUTH)
       
        response_machine_json = response_machine.json()
        
        response_machine_json_value = response_machine_json['values']
        if response_machine_json_value != []:

            for machine in response_machine_json_value:
                visualizationCategory = machine['visualizationCategory']
                productKey = machine['productKey']
                engineSerialNumber = machine['engineSerialNumber']
                telematicsState = machine['telematicsState']
                guid_machine = machine['GUID']
                modelYear = machine['modelYear']
                id_machine = machine['id']
                vin = machine['vin']
                name_machine = machine['name']
                
                insert_value = (visualizationCategory, productKey, engineSerialNumber, telematicsState, guid_machine, modelYear, id_machine, vin, name_machine, id_organizations)
                cursor.execute(sql_query, insert_value)

                print('Data was loaded succesfully ------> ', url_new)

                            
    cnxn.commit()
    cursor.close()
    