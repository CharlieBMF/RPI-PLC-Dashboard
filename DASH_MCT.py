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
full_loop_memory = []
while True:
    starto = time.time()
    for machine_class in list_of_machine_classes:
        try:

            machine_class.dashboard_data_acquisition()
            machine_class.dashboard_data_report_to_sql()
        except:
            continue
    endo = time.time()
    print(f'Full scan time: {endo-starto}')
    time.sleep(0)

