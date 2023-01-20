import pymcprotocol


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
        self.dashboard_data = {}

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

    def dashboard_data_acquisition(self):
        self.connect()
        if self.master_on_address and self.machine_status_address and self.mct_address:
            master_on_value = self.read_bits(head=self.master_on_address)
            machine_status_value = self.read_bits(head=self.machine_status_address)
            mct_value = self.read_words(head=self.mct_address)
            self.dashboard_data = {
                'master_on': master_on_value[0],
                'machine_status': machine_status_value[0],
                'mct': mct_value[0]
            }
        self.close_connection()

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

