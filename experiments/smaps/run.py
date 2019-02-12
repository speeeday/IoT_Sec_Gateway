import argparse
import shlex
import subprocess
import itertools
import time
import os

# Syntax: python start.py -C snort_icmp_block_full -n 4

def start_containers(container, name):
    print name + ":"
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

def print_smaps(name, instances, number):
    cmd='/usr/bin/sudo /usr/bin/docker exec {} bash -c "cat /proc/1/smaps > /root/smaps_snort_{}_{}.txt"'
    cmd=cmd.format(name, instances, number)
    subprocess.check_call(shlex.split(cmd))

def copy_smaps(name, instances, number):
    cmd='/usr/bin/sudo /usr/bin/docker cp {}:/root/smaps_snort_{}_{}.txt /home/pi/IoT_Sec_Gateway/experiments/smaps/'
    cmd=cmd.format(name, instances, number)
    subprocess.check_call(shlex.split(cmd))



def main():
    parser=argparse.ArgumentParser(description='Connect container to vswitch')
    parser.add_argument('--container', '-C', required=True, type=str)
    #    parser.add_argument('--outfile', '-o', required=True, type=str)
    #    parser.add_argument('--name', '-N', required=True, type=str)
    parser.add_argument('--instances', '-n', required=True, type=int)
    args=parser.parse_args()
    name_list = []
    client_ips = []
    server_ips = []
    name_list = get_names(args.instances)

    base_outfile = 'smaps_snort_{}_{}.txt'

    # interval in seconds
    interval = 10
    # delta here to avoid mismeasurement errors
    delta = 4

    start_time = int(time.time())

    # start at (i+2) so that we can get one controlled measurement

    for i in range(0, len(name_list)):

        start_containers(args.container, name_list[i])
        connect_container_dummy(name_list[i])

        time.sleep(interval)


        for j in range(i+1):
            print_smaps(name_list[i], i+1, j+1)
            copy_smaps(name_list[i], i+1, j+1)

    for i in range(0, len(name_list)):
            
        cmd="/usr/bin/sudo /usr/bin/docker stop {}"
        cmd=cmd.format(name_list[i])
        subprocess.call(shlex.split(cmd))

if __name__ == '__main__':
    main()
                                                                                
