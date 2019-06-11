import time

import openzwave
from openzwave.option import ZWaveOption
from openzwave.network import ZWaveNetwork


options = ZWaveOption('/dev/ttyACM0')
options.lock()

network = ZWaveNetwork(options)
# added sleeps here to make sure these commands get flushed
time.sleep(2)
for node in network.nodes:
    for val in network.nodes[node].get_switches():
        network.nodes[node].set_switch(val, True)
        time.sleep(5)
        network.nodes[node].set_switch(val, False)
time.sleep(2)
