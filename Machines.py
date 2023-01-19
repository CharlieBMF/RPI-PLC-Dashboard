import pymcprotocol


class Machine:

    def __init__(self, id_line, id_machine, name, ip, port, target_network=None, plc_id_in_target_network=None):
        self.id_line = id_line
        self.id_machine = id_machine
        self.name = name
        self.ip = ip
        self.port = port
        self.target_network = target_network
        self.plc_id_in_target_network = plc_id_in_target_network
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

    def dashboard_data_acqusition(self, master_on_address=None, machine_status_address=None, mct_address=None):
        if master_on_address and machine_status_address and mct_address:
            master_on_value = self.read_bits(head=master_on_address)
            machine_status_address = self.read_bits(head=machine_status_address)
            mct_address = self.read_words(head=mct_address)
            self.dashboard_data = {'master_on': master_on_value[0],
                                   'machine_status': machine_status_address[0],
                                   'mct': mct_address[0]
                                   }

    def show_info(self):
        print(f'Line: {self.id_line}\n'
              f'Machine: {self.machine}\n'
              f'Name: {self.name}\n'
              f'IP: {self.ip}\n'
              f'PORT: {self.port}\n'
              f'Target other network:{self.target_network}\n'
              f'PLC id in other network: {self.plc_id_in_target_network}'
        )

