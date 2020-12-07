import sys

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology(isVirtual):
    net = Mininet_wifi(controller=Controller)

    info(" ** *Creating nodes\n")
    if isVirtual:
        sta1 = net.addStation('sta1', nvif = 2)
    else:
        sta1 = net.addStation('sta1')
    sta2 = net.addStation('sta2')

    if isVirtual:
        ap1 = net.addAccessPoint('ap1', ssid ="implewifi", mode ="g",  channel ="5")
    else:
        # isolate_clientes: Client isolation can be used to prevent low-level
        # bridging of frames between associated stations in the BSS.
        # By default, this bridging is allowed.
        # OpenFlow rules are required to allow communication among nodes
        ap1 = net.addAccessPoint('ap1', ssid ="implewifi",  isolate_clients = True, mode ="g",  channel ="5")
    c0 = net.addController('c0')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info(" *** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    info(" ** *Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])

    if not isVirtual:
        ap1.cmd('ovs-ofctl add-flow ap1 “priority = 0, arp, in_port = 1, actions = output:in_port, normal"')
        ap1.cmd('ovs-ofctl add-flow ap1 “priority = 0, arp, in_port = 1, actions = output:in_port, normal"')
        ap1.cmd('ovs-ofctl add-flow ap1 “priority = 0, arp, in_port = 1, actions = output:in_port, normal"')
        ap1.cmd('ovs-ofctl add-flow ap1 “priority = 0, arp, in_port = 1, actions = output:in_port, normal"')

        info(" ***Running CLI\n")
        CLI_wifi(net)

        h3 = net.get('sta1')
        h4 = net.get('sta2')

        # h4.cmd( 'ping - c1', h3.IP() )
        h3.cmd('kill % python')
        h4.cmd('kill % python')
        h3.cmd('python server.py &')
        h4.cmd('python client.py % s ' % h3.IP())

        info(" *** Stopping network\n")
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    isVirtual = True if '-v' in sys.argv else False
    topology(isVirtual)
