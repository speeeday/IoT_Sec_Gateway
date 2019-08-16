#!/bin/bash

while true; do
    grep -q '^1$' "/sys/class/net/eth0/carrier" &&
	grep -q '^1$' "/sys/class/net/eth1/carrier" &&
	grep -q '^1$' "/sys/class/net/eth2/carrier" &&
	break

    sleep 1

done

cd /testvolume/daq-2.0.6
make install

cd /testvolume/snort-client
make install

LD_LIBRARY_PATH="/usr/local/lib" /testvolume/snort-client/src/snort "$@"
#exec /bin/bash
