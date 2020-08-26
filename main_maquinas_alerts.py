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
    sql_query = ''' INSERT INTO alertas( type_alert, duration_value, duration_unit, occurrences, engineHours_value, engineHours_unit, machineLinearTime, bus, id_alert, time_alert, color, severity, acknowledgementStatus, ignored, invisible, id_machine)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    url= 'https://sandboxapi.deere.com/platform/organizations'
    url1= 'https://sandboxapi.deere.com/platform'

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

        #Existen organizaciones que no tienen máquinas las filtramos aca
        if response_machine_json_value != []:

            for machine in response_machine_json_value:
                
                id_machine = machine['id']
                
                url_newest = url1 + '/machines/' +id_machine + '/alerts'
                print(url_newest)
                response_alerts_json = request_test(url_newest, headers, AUTH)
                response_alerts_value = response_alerts_json['values']
                print(response_alerts_value)

                #Exiten máquienas que no tienen alertas
                if response_alerts_value != []:

                    for alert in response_alerts_value:
                        type_alert = alert['@type']
                        duration_value = alert['duration']['valueAsInteger']
                        duration_unit = alert['duration']['unit']
                        occurrences = alert['occurrences']
                        engineHours_value = alert['engineHours']['reading']['valueAsDouble']
                        engineHours_unit = alert['engineHours']['reading']['unit']
                        machineLinearTime = alert['machineLinearTime']
                        bus = alert['bus']
                        id_alert = alert['id']
                        time_alert = alert['time']
                        color = alert['color']
                        severity =alert['severity']
                        acknowledgementStatus =alert['acknowledgementStatus']
                        ignored =alert['ignored']
                        invisible =alert['invisible']
                        
                        insert_value = (type_alert, duration_value, duration_unit, occurrences, engineHours_value, engineHours_unit, machineLinearTime, bus, id_alert, time_alert, color, severity, acknowledgementStatus, ignored, invisible, id_machine) 
                        insert_value = (visualizationCategory, productKey, engineSerialNumber, telematicsState, guid_machine, modelYear, id_machine, vin, name_machine, id_organizations)
                        cursor.execute(sql_query, insert_value)

                        print('Data was loaded succesfully: ', id_alert)

                else:
                    print('Esta máquia no tiene alertas: ', id_machine)

                            
    cnxn.commit()
    cursor.close()
    