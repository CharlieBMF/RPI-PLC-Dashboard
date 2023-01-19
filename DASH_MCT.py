import os
import time
import pyodbc
import pandas as pd
from Machines import Machine


print('Started at..', os.path.dirname(os.path.abspath(__file__)))
Housing_Assembly = Machine(name='HA', ip='192.168.10.201', port=40020)


while True:
    Housing_Assembly.connect()
    OK_Counter = Housing_Assembly.read_words(head='D50122')
    print(f'Licznik sztuk OK: {OK_Counter[0]}')
    Housing_Assembly.close_connection()

    cnxn = pyodbc.connect('DRIVER=FreeTDS;SERVER=159.228.208.243;PORT=1433;DATABASE=mapsData;UID=sa;PWD=Daicel@DSSE;Encrypt=no',timeout=1)

    data = pd.read_sql("SELECT TOP(100) * FROM tMapsMCTs", cnxn)
    print(data)
    del cnxn
    time.sleep(5)


#     conn = pg2.connect(database='dvdrental', user='postgres', password='zaq12wsx')
#     cur = conn.cursor()
#     cur.execute(f'INSERT INTO oks(machineid, ok) VALUES(1,{OK_Counter[0]})')
#     conn.commit()
#     conn.close()
#
#     time.sleep(5)
