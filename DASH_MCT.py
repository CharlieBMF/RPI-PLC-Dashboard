import os
import time
import pyodbc
import pandas as pd
from Machines import Machine
from conf import machines_names


def create_machine_classes():
    list = []
    for k, v in machines_names.items():
        k = Machine(id_line=v['id_line'], id_machine=v['id_machine'], name=v['name'], ip=v['ip'], port=v['port'])
        list.append(k)
    return list


print('Started at..', os.path.dirname(os.path.abspath(__file__)))
list_of_machine_classes = create_machine_classes()



while True:
    Housing_Assembly.connect()
    Housing_Assembly.dashboard_data_acqusition(master_on_address='M6',
                                               machine_status_address='M44',
                                               mct_address='D50080')
    Housing_Assembly.close_connection()
    print(Housing_Assembly.dashboard_data['master_on'],
          Housing_Assembly.dashboard_data['machine_status'],
          Housing_Assembly.dashboard_data['mct'])

    cnxn = pyodbc.connect(
        'DRIVER=FreeTDS;SERVER=159.228.208.243;PORT=1433;DATABASE=mapsData;UID=python;PWD=Daicel@DSSE;Encrypt=no',
        timeout=1
    )
    cursor = cnxn.cursor()
    cursor.execute(f'INSERT INTO tMapsMCTs (idLine,idMachines,MCT) VALUES ({Housing_Assembly.id_line},'
                   f'{Housing_Assembly.id_machine},{Housing_Assembly.dashboard_data["mct"]})')
    cnxn.commit()
    data = pd.read_sql("SELECT TOP(100) * FROM tMapsMCTs ORDER BY ReportDate DESC", cnxn)
    del cnxn
    print(data)

    time.sleep(5)

