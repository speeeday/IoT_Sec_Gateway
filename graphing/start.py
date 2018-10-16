import argparse
import shlex
import subprocess
import itertools
import time
import os

# Syntax: python start.py -C snort_icmp_block -n 4

def start_containers(container, name):
    cmd='/usr/bin/sudo /usr/bin/docker run -itd --rm --name {} {}'
    cmd=cmd.format(name, container)
    subprocess.check_call(shlex.split(cmd))

def connect_container_dummy(container_name):
    cmd='/usr/bin/sudo /usr/bin/docker network connect network2 {}'
    cmd=cmd.format(container_name)
    subprocess.check_call(shlex.split(cmd))

def get_names(number):
    list=['test{}'.format(i) for i in range(number)]
    return list

def main():
    parser=argparse.ArgumentParser(description='Connect container to vswitch')
    parser.add_argument('--container', '-C', required=True, type=str)
    parser.add_argument('--outfile', '-o', required=True, type=str)
#    parser.add_argument('--name', '-N', required=True, type=str)
    parser.add_argument('--instances', '-n', required=True, type=int)
    args=parser.parse_args()
    name_list = []
    client_ips = []
    server_ips = []
    name_list = get_names(args.instances)

    # interval in seconds
    interval = 30
    # delta here to avoid mismeasurement errors
    delta = 4
    
    # start the lsof cmd in the background
#    cmd='/usr/bin/sudo /usr/bin/lsof -r {} -F 0 > {} &'
    cmd = '/usr/bin/sudo python dump_meminfo.py {} {} &'
    cmd=cmd.format(interval, args.outfile)
    os.system(cmd);

    start_time = int(time.time())

    # start at (i+2) so that we can get one controlled measurement

    for i in range(0, len(name_list)):
        while int(time.time()) <= ((start_time + (i+2)*interval) + delta):
            time.sleep(2)
        start_containers(args.container, name_list[i])
        connect_container_dummy(name_list[i])

    # wait to get the last stats
    while int(time.time()) <= ((start_time + (len(name_list)+2)*interval) + delta):
        time.sleep(2)

    #cmd='/usr/bin/sudo /usr/bin/killall lsof'
    #subprocess.call(shlex.split(cmd))

    cmd='/usr/bin/sudo /usr/bin/killall python'
    subprocess.call(shlex.split(cmd))

if __name__ == '__main__':
    main()
    

