import pandas as pd
from django.shortcuts import render
from django.urls import reverse
import pyodbc
import pandas as pd
import sys
sys.path.append('/home/pi/Scripts')
from conf import machines_names


def main(request):
    cnxn = pyodbc.connect(
        'DRIVER=FreeTDS;'
        'SERVER=159.228.208.243;'
        'PORT=1433;'
        'DATABASE=mapsData;'
        'UID=python;'
        'PWD=Daicel@DSSE;Encrypt=no',
        timeout=1
    )

    answer = {}
    data = pd.read_sql("select * from tMachinesForMaps WHERE (idLine=32 OR idLine=33)", cnxn)
    del cnxn
    for machine in machines_names.keys():
        answer[machine] = {'MasterOn': data[data['id'] == machines_names[machine]['id_machine']].iloc[0]['MasterOn'],
                           'AutoStart': data[data['id'] == machines_names[machine]['id_machine']].iloc[0]['AutoStart'],
                           'mct': data[data['id'] == machines_names[machine]['id_machine']].iloc[0]['RealMCT']}
        print(answer)

    return render(request, 'dashboard_mct_new.html', answer)


