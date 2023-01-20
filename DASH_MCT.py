import os
import time
import pyodbc
import pandas as pd
from Machines import Machine
from conf import machines_names


def create_machine_classes():
    list_of_machines = []
    for k, v in machines_names.items():
        k = Machine(id_line=v['id_line'], id_machine=v['id_machine'], name=v['name'], ip=v['ip'], port=v['port'],
                    master_on_address=v['address']['master_on_address'],
                    machine_status_address=v['address']['machine_status_address'],
                    mct_address=v['address']['mct_address'])
        list_of_machines.append(k)
    return list_of_machines


print('Started at..', os.path.dirname(os.path.abspath(__file__)))
list_of_machine_classes = create_machine_classes()

while True:
    for machine_class in list_of_machine_classes:
        try:
            machine_class.connect()
        except:
            continue
        else:
            machine_class.dashboard_data_acquisition()
            machine_class.connection_data_display()
            machine_class.dashboard_data_display()
            print('\n'*2)



    # cnxn = pyodbc.connect(
    #     'DRIVER=FreeTDS;SERVER=159.228.208.243;PORT=1433;DATABASE=mapsData;UID=python;PWD=Daicel@DSSE;Encrypt=no',
    #     timeout=1
    # )
    # cursor = cnxn.cursor()
    # cursor.execute(f'INSERT INTO tMapsMCTs (idLine,idMachines,MCT) VALUES ({Housing_Assembly.id_line},'
    #                f'{Housing_Assembly.id_machine},{Housing_Assembly.dashboard_data["mct"]})')
    # cnxn.commit()
    # data = pd.read_sql("SELECT TOP(100) * FROM tMapsMCTs ORDER BY ReportDate DESC", cnxn)
    # del cnxn
    # print(data)

    time.sleep(5)

