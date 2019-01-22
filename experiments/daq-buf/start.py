import argparse
import shlex
import subprocess
import itertools
import time
import os

# Syntax: python start.py -C snort_icmp_block -n 4

cname = 'test1'

def build_container(path, container):
#    sudo docker build -t="snort_icmp_block" /home/sj/research-projects/scalable-dataplane/IoT_Sec_Gateway/docker_containers/snort_icmp_block/

def start_containers(container, name):
    cmd='/usr/bin/sudo /usr/bin/docker run -itd --rm --name {} {}'
    cmd=cmd.format(name, container)
    subprocess.check_call(shlex.split(cmd))

def connect_container_dummy(container_name):
    cmd='/usr/bin/sudo /usr/bin/docker network connect network2 {}'
    cmd=cmd.format(container_name)
    subprocess.check_call(shlex.split(cmd))

def kill_container(container_name):
    cmd='/usr/bin/sudo /usr/bin/docker kill {}'
    cmd=cmd.format(container_name)
    subprocess.call(shlex.split(cmd))
    
    
def get_names(number):
    list=['test{}'.format(i) for i in range(number)]
    return list

def main():
    parser=argparse.ArgumentParser(description='Connect container to vswitch')
    parser.add_argument('--container', '-C', required=True, type=str)
    parser.add_argument('--outfile', '-o', required=True, type=str)
    parser.add_argument('--instances', '-n', required=True, type=int)
    args=parser.parse_args()
    name_list = []
    client_ips = []
    server_ips = []
    name_list = get_names(args.instances)

    # interval in seconds
    interval = 10
    # delta here to avoid mismeasurement errors
    delta = 4


    # start at (i+2) so that we can get one controlled measurement

    for i in range(0, len(name_list)):

        os.system('sudo cat /proc/meminfo >> %s' % (args.outfile + '-meminfo'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-meminfo'))
        
        os.system('sudo free >> %s' % (args.outfile + '-free'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-free'))
        
        os.system('sudo echo %d >> %s' % (0, (args.outfile + '-time')))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-time'))
        
    
        time.sleep(interval/2)
        
        start_time = int(time.time())
        
        start_containers(args.container, name_list[i])
        connect_container_dummy(name_list[i])

        end_time = time.time()
        time.sleep(interval)
        
        os.system('sudo cat /proc/meminfo >> %s' % (args.outfile + '-meminfo'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-meminfo'))

        os.system('sudo free >> %s' % (args.outfile + '-free'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-free'))

        os.system('sudo echo %d >> %s' % ((end_time - start_time), (args.outfile + '-time')))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-time'))
        
        time.sleep(interval/2)

    cmd='/usr/bin/sudo /usr/bin/killall python'
    subprocess.call(shlex.split(cmd))

if __name__ == '__main__':
    main()
    

