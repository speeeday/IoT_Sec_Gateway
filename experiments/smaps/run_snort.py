import argparse
import shlex
import subprocess
import itertools
import time
import os
# Syntax: python start.py -C snort_icmp_block_full -n 4

container_name = 'snort_test'

def start_container(container, name):
    print container_name + ":"
    cmd='/usr/bin/sudo /usr/bin/docker run -itd --rm --name {} {}'
    cmd=cmd.format(container_name, container)
    subprocess.check_call(shlex.split(cmd))

def connect_container_dummy(container_name):
    cmd='/usr/bin/sudo /usr/bin/docker network connect network2 {}'
    cmd=cmd.format(container_name)
    subprocess.check_call(shlex.split(cmd))

def get_names(number):
    list=['test{}'.format(i) for i in range(number)]
    return list

def print_smaps(name, instances, number):
    # sudo docker exec -it testing bash -c "cat /root/{}/snort_eth0:eth1.pid" > p    .format(name)

    # read the file p
    cmd='sudo docker cp {}:/root/{}/snort_eth0:eth1.pid /home/pi/IoT_Sec_Gateway/experiments/smaps/p'
    #cmd='sudo docker exec -it {} bash -c "cat /root/{}/snort_eth0:eth1.pid" > p'
    cmd=cmd.format(container_name, name)
    subprocess.check_call(shlex.split(cmd))

    pid = int(open('p').read())
    cmd='/usr/bin/sudo /usr/bin/docker exec {} bash -c "cat /proc/{}/smaps > /root/smaps_snort_{}_{}.txt"'
    cmd=cmd.format(container_name, pid, instances, number)
    subprocess.check_call(shlex.split(cmd))

def copy_smaps(name, instances, number):
    cmd='/usr/bin/sudo /usr/bin/docker cp {}:/root/smaps_snort_{}_{}.txt /home/pi/IoT_Sec_Gateway/experiments/smaps/'
    cmd=cmd.format(container_name, instances, number)
    subprocess.check_call(shlex.split(cmd))


def start_snort(dir_name):
    # "-Q", "--daq", "afpacket", "--daq-var", "buffer_size_mb=1", "-i", "eth0:eth1", "-c", "/etc/snort/etc/snort.conf", "-l", "/var/log/snort/"]
    # /usr/local/bin/snort
#sudo docker exec -itd testing /usr/local/bin/snort -Q --daq afpacket --daq-var buffer_size_mb=1 -i eth0:eth1 -c /etc/snort/etc/snort.conf -l /var/log/snort
    cmd='sudo docker exec -itd {} /usr/local/bin/snort -Q --daq afpacket --daq-var buffer_size_mb=1 -i eth0:eth1 -c /etc/snort/etc/snort.conf -l /var/log/snort --pid-path /root/{}/'
    cmd=cmd.format(container_name, dir_name)
    subprocess.check_call(shlex.split(cmd))
    
def main():
    parser=argparse.ArgumentParser(description='Connect container to vswitch')
    parser.add_argument('--container', '-C', required=True, type=str)
    parser.add_argument('--instances', '-n', required=True, type=int)

    args=parser.parse_args()

    name_list = []
    name_list = get_names(args.instances)

    base_outfile = 'smaps_snort_{}_{}.txt'

    # interval in seconds
    interval = 30
    # delta here to avoid mismeasurement errors
    delta = 4

    start_time = int(time.time())

    start_container(args.container, container_name)
    connect_container_dummy(container_name)
    
    # sudo docker exec -itd {} bash -c "mkdir -p /root/{}    .format(container_name, name_list[0])
    cmd='sudo docker exec -itd {} bash -c "mkdir -p /root/{}"'
    cmd=cmd.format(container_name, name_list[0])
    subprocess.call(shlex.split(cmd))

    cmd='sudo docker exec -itd {} bash -c "echo 1 > /root/{}/snort_eth0:eth1.pid"'
    cmd=cmd.format(container_name, name_list[0])
    subprocess.call(shlex.split(cmd))
    
    #os.system('mkdir -p ' + name_list[0])
    #os.system('echo 1 > ' + name_list[0] + '/snort_eth0:eth1.pid')
    print_smaps(name_list[0], 1, 1)
    copy_smaps(name_list[0], 1, 1)

    print "Started " + name_list[0]
    
    for i in range(1, len(name_list)):
        # sudo docker exec -itd {} bash -c "mkdir -p /root/{}    .format(container_name, name_list[0])
        cmd='sudo docker exec -itd {} bash -c "mkdir -p /root/{}"'
        cmd=cmd.format(container_name, name_list[i])
        subprocess.call(shlex.split(cmd))

    # sudo docker exec -itd {} bash -c "mkdir -p /root/{}/    .format(container_name, name_list[i])
        #os.system('mkdir -p ' + name_list[i])
        
        start_snort(name_list[i])
        print "Started " + name_list[i]

        time.sleep(interval)


        for j in range(i+1):
            print_smaps(name_list[i], i+1, j+1)
            copy_smaps(name_list[i], i+1, j+1)

            
    cmd="/usr/bin/sudo /usr/bin/docker stop {}"
    cmd=cmd.format(container_name)
    subprocess.call(shlex.split(cmd))

if __name__ == '__main__':
    main()
                                                                                
