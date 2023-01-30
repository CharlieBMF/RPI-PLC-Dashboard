# RPI-PLC-Dashboard
Acquiring data from PLC in factory, store it in server SQL and visualise as dashboards on production line TV using django

<h1> Details </h1>
<h2> Hardware </h2>
<ul>
<li> Raspberry Pi 4B </li>
<li> TV </li>
<li> PLC Mitsubishi series Q with ETH </li>
</ul>
<h2> Operation diagram </h2>
<h3> Configuring PLC </h3>
First of all it is necessary to open ports in PLC CPU for connection. In this example port 40020 is used.
<img src="https://user-images.githubusercontent.com/109242797/215436365-18a7d392-62d1-42b1-a8b7-d52269cf5d4a.png" alt='not found' title='PLC Config'>
<br>
It is necessary to configure ETH adress in PLC module.
<img src="https://user-images.githubusercontent.com/109242797/215436968-08f8fbd3-957b-4913-9187-3d67020528dd.png" alt='not found' title='PLC Config'>
<h3> Configure machines in conf.py </h3>
All machines should be configured in conf.py as:
<ol>
<li> id_line - line id for each machine </li>
<li> id_machine - unique machine id </li>
<li> name - name of the machine </li>
<li> ip - IP Adress for machine </li>
<li> port - open port for connection to the machine </li>
<li> address - contains addresses in PLC which will be used in data acquisition, in this case it is Power On, Auto Start and MCT (Machine Cycle Time) value </li>
<li> target_network - script could read a data from diffrent networ than connected ETH. It could switch to fiber after connecting to PLC and use data from different machine in any network number. This parameter is network number. N/A this case </li>
<li> plc_id_in_target_network - id for the PLC in additionan network. N/A this case </li>
</ol>
<img src="https://user-images.githubusercontent.com/109242797/215438679-be4c40dd-86bf-4980-adaf-1165994109d6.png" alt='not found' title='conf.py'>
<h3> Configure DASH_MCT.py </h3>
Each machine configured in conf.py starts a class in DASH_MCT.py. 
Operation diagram looks like:
<ol>
<li> Connect to PLC using IP Adress, port and pymcprotocol </li>
<li> Read a data from PLC and addreses configured in conf.py using pymcprotocol </li>
<li> Store a data and check if it is different than last one </li>
<li> If data is different connect to database and store new data </li>
</ol>

<h2> Dashboard </h2>
Second step is creating a dashboard visualization for TV/PC etc.
Dashboard shows each machine and actual status. This facilitates line operation, control of process parameters and line management. Django is used for this.
<img src="https://user-images.githubusercontent.com/109242797/215440336-05ffdddf-73c8-4da2-b1e4-e456a45f824a.png" alt='not found' title='dashboard_on_monitor'>

