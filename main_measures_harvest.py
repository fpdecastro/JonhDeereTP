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
    sql_query = ''' INSERT INTO med_harvest(measurementName, area_value, area_unit, yield_value, yield_unit, averageYield_value, averageYield_unit, averageMoisture_value, averageMoisture_unit, wetMass_value, wetMass_unit, averageWetMass_value, averageWetMass_unit, averageSpeed_value, averageSpeed_unit, id_operation)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    url= 'https://sandboxapi.deere.com/platform/organizations'
    uri = 'https://sandboxapi.deere.com/platform'
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
                    print('field: ', field_id)
                    url_newest_operation = url + '/' + id_organizations + '/fields/' + field_id + '/fieldOperations' 
                    
                    response_operation_json = request_test(url_newest_operation, headers, AUTH)
                    
                    response_operation_value = response_operation_json['values']
                    if response_operation_value != []:
                        for operation in response_operation_value:

                            id_operation = operation['id']
                            print('operation: ', id_operation)

                            fieldOperationType = operation['fieldOperationType']

                            if fieldOperationType == 'harvest':

                                url_newest_measures = uri + '/fieldOperations/' + id_operation + '/measurementTypes'
                                response_measure_json = request_test(url_newest_measures, headers, AUTH)
                                response_measure_value = response_measure_json['values']

                                for measures in response_measure_value:
                                    measurementName = measures['measurementName']
                                    area_value = measures['area']['value']
                                    area_unit = measures['area']['unitId']
                                    yield_value = measures['yield']['value']
                                    yield_unit = measures['yield']['unitId']
                                    averageYield_value = measures['averageYield']['value']
                                    averageYield_unit = measures['averageYield']['unitId']
                                    averageMoisture_value = measures['averageMoisture']['value']
                                    averageMoisture_unit = measures['averageMoisture']['unitId']
                                    wetMass_value = measures['wetMass']['value']
                                    wetMass_unit = measures['wetMass']['unitId']
                                    averageWetMass_value = measures['averageWetMass']['value']
                                    averageWetMass_unit = measures['averageWetMass']['unitId']
                                    averageSpeed_value = measures['averageSpeed']['value']
                                    averageSpeed_unit = measures['averageSpeed']['unitId']
                                    
                                    insert_values = (measurementName, area_value, area_unit, yield_value, yield_unit, averageYield_value, averageYield_unit, averageMoisture_value, averageMoisture_unit, wetMass_value, wetMass_unit, averageWetMass_value, averageWetMass_unit, averageSpeed_value, averageSpeed_unit, id_operation)
                                    
                                    cursor.execute(sql_query, insert_values)
                                    
                                    print('Data was loaded succesfully ------> ', url_newest_measures)

                            
                            
                            else:
                                print('No se encontro una operación harvest')

                                
    cnxn.commit()
    
    cursor.close()

    

    
    


