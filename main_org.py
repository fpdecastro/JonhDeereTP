import requests
from requests_oauthlib import OAuth1
import pyodbc

headers = {
    'Accept' : 'application/vnd.deere.axiom.v3+json'
}

consumer_key = 'johndeere-JcFsHU6CV0klrsgkDHewTLuSAP1QZ2Q8Tx9sFCOs' 
consumer_secret = '5b67d63b58a9e80facb93354b18a79eb9be3b668f02e331cace8f5a4190254fa'
token = 'd8d3c1b7-8f56-4cc3-96a6-0b6da898eea6'
token_secret = '19Ryi+uXOFxS3/8Q0h+pHjlGVXaYndLhTOl64Wg4cdA4/5ly0f48DxcN+nBsfFgXP71ruvCHMb4T5fYXeGzQ5uAzGYDKyfONgE0Mp6y1bbA='

# Defino el servidor y la base de datos
server = 'DESKTOP-FP2QGMT\MSSQL2014' 
database = 'JohnDeere'

if __name__ == "__main__":
    # Me conecto a la base de datos
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ server +'; DATABASE='+ database +'; Trusted_Connection=yes;')
    
    #Creo la connection al cursor
    cursor = cnxn.cursor()
    
    #Definimos le script en SQL
    sql_query = ''' INSERT INTO organizacion(id_org, name, type_org, member)
                    VALUES (?, ?, ?, ?)'''

    url= 'https://sandboxapi.deere.com/platform/organizations'
    auth = OAuth1(consumer_key, consumer_secret,token, token_secret)
    
    response = requests.get(url, headers=headers ,auth=auth)
    # Recibo el request y lo transformo a json()
    response_json = response.json()
    # Recibo un diccionario y necesito values
    response_values = response_json['values']
    # itero para ver los nombres
    for organizations in response_values:
        insert_values = (organizations['id'], organizations['name'], organizations['type'], organizations['member'])
        cursor.execute(sql_query, insert_values)
    cnxn.commit()
    cursor.close()
    