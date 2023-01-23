import pymcprotocol
import pyodbc
import time


def time_wrapper(func):
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        if end-start > 1:
            print(f'Func {func.__name__} started: {start} finished: {end} Time: {end-start}')
        return result
    return wrap


class Machine:

    def __init__(self, id_line, id_machine, name, ip, port, master_on_address, machine_status_address, mct_address,
                 target_network=None, plc_id_in_target_network=None,):
        self.id_line = id_line
        self.id_machine = id_machine
        self.name = name
        self.ip = ip
        self.port = port
        self.target_network = target_network
        self.plc_id_in_target_network = plc_id_in_target_network
        self.master_on_address = master_on_address
        self.machine_status_address = machine_status_address
        self.mct_address = mct_address
        self.machine = self.define_machine_root()
        self.dashboard_data = {'master_on': 0, 'machine_status': 0, 'mct': 0}
        self.dashboard_data_report_request = {'master_on': False, 'machine_status': False, 'mct': False}

    def define_machine_root(self):
        pymc3e = pymcprotocol.Type3E()
        if self.target_network and self.plc_id_in_target_network:
            pymc3e.network = self.target_network
            pymc3e.pc = self.plc_id_in_target_network
        return pymc3e

    def connect(self):
        self.machine.connect(ip=self.ip, port=self.port)

    def close_connection(self):
        self.machine.close()

    def read_bits(self, head, size=1):
        return self.machine.batchread_bitunits(headdevice=head, readsize=size)

    def read_words(self, head, size=1):
        return self.machine.batchread_wordunits(headdevice=head, readsize=size)

    def read_random_words(self, word_devices, double_word_devices):
        return self.machine.randomread(word_devices=word_devices, dword_devices=double_word_devices)

    @time_wrapper
    def dashboard_data_acquisition(self):
        self.connect()
        if self.master_on_address and self.machine_status_address and self.mct_address:
            master_on_value = self.read_bits(head=self.master_on_address)
            machine_status_value = self.read_bits(head=self.machine_status_address)
            mct_value = self.read_words(head=self.mct_address)
            self.dashboard_data_set_report_requests(master_on_value=master_on_value[0],
                                                    machine_status_value=machine_status_value[0],
                                                    mct_value=mct_value[0])
            self.dashboard_data = {
                'master_on': master_on_value[0],
                'machine_status': machine_status_value[0],
                'mct': mct_value[0]
            }
        self.close_connection()

    def dashboard_data_set_report_requests(self, master_on_value, machine_status_value, mct_value):
        if master_on_value != self.dashboard_data['master_on']:
            self.dashboard_data_report_request['master_on'] = True
        if machine_status_value != self.dashboard_data['machine_status']:
            self.dashboard_data_report_request['machine_status'] = True
        if mct_value != self.dashboard_data['mct']:
            self.dashboard_data_report_request['mct'] = True

    def dashboard_data_report_to_sql(self):
        if self.dashboard_data_report_request['master_on'] or self.dashboard_data_report_request['machine_status']:
            string = f'INSERT INTO tMapsMachineStatus (idLine,idMachines,MasterOn,AutoStart) VALUES ' \
                     f'({self.id_line}, ' \
                     f'{self.id_machine}, ' \
                     f'{self.dashboard_data["master_on"]},' \
                     f' {self.dashboard_data["machine_status"]})'
            self.sql_execute_insert(string)
        if self.dashboard_data_report_request['mct']:
            string = f'INSERT INTO tMapsMCTs (idLine,idMachines,MCT) VALUES ' \
                     f'({self.id_line}, ' \
                     f'{self.id_machine}, ' \
                     f'{self.dashboard_data["mct"]})'
            self.sql_execute_insert(string)

    @time_wrapper
    def sql_execute_insert(self, string):
        cnxn = pyodbc.connect(
            'DRIVER=FreeTDS;'
            'SERVER=159.228.208.243;'
            'PORT=1433;'
            'DATABASE=mapsData;'
            'UID=python;'
            'PWD=Daicel@DSSE;Encrypt=no',
            timeout=1
        )
        cursor = cnxn.cursor()
        cursor.execute(string)
        cnxn.commit()
        del cnxn
        if 'tMapsMachineStatus' in string:
            self.dashboard_data_report_request['master_on'] = False
            self.dashboard_data_report_request['machine_status'] = False
            print(f'Reported (master on) (machine status) on {self.name}')
        elif 'tMapsMCTs' in string:
            self.dashboard_data_report_request['mct'] = False
            print(f'Reported (mct) on {self.name}')

    def dashboard_data_display(self):
        print(
            f'/'*20,
            f'\nMASTER ON: {self.dashboard_data["master_on"]}\n'
            f'AUTO START: {self.dashboard_data["machine_status"]}\n'
            f'MCT: {self.dashboard_data["mct"]}\n'
        )

    def connection_data_display(self):
        print(
            '*'*20,
            f'\nLine: {self.id_line}\n'
            f'Machine: {self.id_machine}\n'
            f'Name: {self.name}\n'
            f'IP: {self.ip}\n'
            f'PORT: {self.port}\n'
            f'Target other network: {self.target_network}\n'
            f'PLC id in other network: {self.plc_id_in_target_network}\n'
        )

