#!/usr/bin/python
import os
from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP, UserAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from time import sleep
from mininet.net import Mininet

carNumber = 10


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, accessPoint=OVSKernelAP, link=wmediumd, wmediumd_mode=interference)
    # net = Mininet_wifi(controller=Controller, accessPoint=UserAP, link=wmediumd, wmediumd_mode=interference)
    info("*** Creating nodes\n")
    cars = []
    for id in range(0, carNumber):
        cars.append(net.addCar('car%s' % (id + 1), wlans=2))

    e1 = net.addAccessPoint('e1', ssid='vanet-ssid', mac='00:00:00:11:00:01', mode='g', channel='1',
                            position='3279.02,3736.27,0', range='55000')
    e2 = net.addAccessPoint('e2', ssid='vanet-ssid', mac='00:00:00:11:00:02', mode='g', channel='6',
                            position='2320.82,3565.75,0', range='55000')
    e3 = net.addAccessPoint('e3', ssid='vanet-ssid', mac='00:00:00:11:00:03', mode='g', channel='11',
                            position='2806.42,3395.22,0', range='55000')
    e4 = net.addAccessPoint('e4', ssid='vanet-ssid', mac='00:00:00:11:00:04', mode='g', channel='1',
                            position='3332.62,3253.92,0', range='55000')
    e5 = net.addAccessPoint('e5', ssid='vanet-ssid', mac='00:00:00:11:00:05', mode='g', channel='6',
                            position='2887.62,2935.61,0', range='55000')
    e6 = net.addAccessPoint('e6', ssid='vanet-ssid', mac='00:00:00:11:00:06', mode='g', channel='11',
                            position='2351.68,3083.40,0', range='55000')
    switch = net.addSwitch('switch', dpid='52000000000')
    c1 = net.addController('c1')
    server = net.addHost('server', ip='192.168.0.250/24')

    info("*** Setting bgscan\n")
    # net.setBgscan(signal=-45, s_inverval=5, l_interval=10)
    net.setBgscan(signal=-90, s_inverval=5, l_interval=10)  # new
    info("*** Configuring Propagation Model\n")
    # net.setPropagationModel(model="logDistance", exp=2)
    net.setPropagationModel(model="logDistance", exp=2)  # new
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.addLink(e1, switch)
    net.addLink(e2, switch)
    net.addLink(e3, switch)
    net.addLink(e4, switch)
    net.addLink(e5, switch)
    net.addLink(e6, switch)
    net.addLink(server, switch)


info("*** Configuring wifi nodes\n")
net.configureWifiNodes()
net.addLink(e1, switch)
net.addLink(e2, switch)
net.addLink(e3, switch)
net.addLink(e4, switch)
net.addLink(e5, switch)
net.addLink(e6, switch)
net.addLink(server, switch)

for car in cars:
    net.addLink(car, intf=car.params['wlan'][1], cls=mesh, ssid='mesh-ssid', channel=5)
net.useExternalProgram(program=sumo, port=8813, config_file='map.sumocfg')
info("*** Starting network\n")
net.build()
c1.start()
switch.start([c1])
e1.start([c1])
e2.start([c1])
e3.start([c1])
e4.start([c1])
e5.start([c1])
e6.start([c1])

for car in cars:
    car.setIP('192.168.0.%s/24' % (int(cars.index(car)) + 1), intf='%s-wlan0' % car)
car.setIP('192.168.1.%s/24' % (int(cars.index(car)) + 1), intf='%s-mp1' % car)

print("Play SUMO.")
print("Execute o Servidor Iperf")

CLI_wifi(net)

print("Todos os carros, menos o car1, disparando pro servidor...")

for x in range(carNumber):
    if (x != 0):
        print(x)

print(carNumber)
print(net.get('car%s' % (x + 1)))

net.get('car%s' % (x + 1)).cmd('iperf -c 192.168.0.250 -u -b 27M -y c -t 2000 &')

for x in range(15):
    net.get('car1').cmd('iperf -c 192.168.0.250 -u -b 27M -y c -t 15 ')
sleep(3)

print("finalizando experimento...")
CLI_wifi(net)

info("Matando processos em segundo plano...")
print("\n")

for x in range(0, carNumber):
    if (x != 0):
        net.get('car%s' % (x + 1)).cmd('kill %while')
pid = int(net.get('car%s' % (x + 1)).cmd('echo $!'))
print(x + 1)
print(pid)

net.get('car%s' % (x + 1)).cmd('kill -9 %i' % pid)
info("Todos os processos terminaram")
info("*** Stopping network\n")
net.stop()
