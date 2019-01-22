import argparse
import shlex
import subprocess
import itertools
import time
import os

# Syntax: python start.py -C snort_icmp_block -n 4

cname = 'test1'

def rebuild_container(size):
    # replace line 69 in Dockerfile
    # CMD ["-Q", "--daq", "afpacket", "--daq-var", "buffer_size_mb={}", "-i", "eth0:eth1", "-c", "/etc/snort/snort.conf", "-l", "/var/log/snort/"]
    linenum = 69
    base_cmd = '/bin/sed \'{}s/.*/CMD ["-Q", "--daq", "afpacket", "--daq-var", "buffer_size_mb={}", "-i", "eth0:eth1", "-c", "/etc/snort/snort.conf", "-l", "/var/log/snort/"]\' snort_daq_buf_test/Dockerfile'
    cmd=base_cmd.format(linenum, size)
    subprocess.check_call(shlex.split(cmd))

#    sudo docker build -t="snort_icmp_block" /home/sj/research-projects/scalable-dataplane/IoT_Sec_Gateway/docker_containers/snort_icmp_block/
    cmd='/usr/bin/sudo /usr/bin/docker build -t="snort_daq_buf_test" snort_daq_buf_test/'
    subprocess.check_call(shlex.split(cmd))
    
    

def start_container(name):
    cmd='/usr/bin/sudo /usr/bin/docker run -itd --rm --name {} {}'
    cmd=cmd.format(name, 'snort_daq_buf_test')
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
    parser.add_argument('--outfile', '-o', required=True, type=str)
    args=parser.parse_args()

    # daq buffer sizes to try
    size_list = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 40, 80, 128] #128 is default

    # interval in seconds
    interval = 10
    # delta here to avoid mismeasurement errors
    delta = 4


    # start at (i+2) so that we can get one controlled measurement

    for i in range(0, len(size_list)):

        os.system('sudo cat /proc/meminfo >> %s' % (args.outfile + '-meminfo'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-meminfo'))
        
        os.system('sudo free >> %s' % (args.outfile + '-free'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-free'))
        
        os.system('sudo echo %d >> %s' % (0, (args.outfile + '-time')))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-time'))
        
    
        time.sleep(interval/4)
        
        start_time = int(time.time())

        rebuild_container(size_list[i])
        start_container(cname)
        connect_container_dummy(cname)
        
        end_time = time.time()
        time.sleep(interval)
        
        os.system('sudo cat /proc/meminfo >> %s' % (args.outfile + '-meminfo'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-meminfo'))

        os.system('sudo free >> %s' % (args.outfile + '-free'))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-free'))

        os.system('sudo echo %d >> %s' % ((end_time - start_time), (args.outfile + '-time')))
        os.system('sudo echo "==========" >> %s' % (args.outfile + '-time'))
        
        time.sleep(interval/4)

        kill_container(cname)

        time.sleep(interval/2)


    cmd='/usr/bin/sudo /usr/bin/killall python'
    subprocess.call(shlex.split(cmd))

if __name__ == '__main__':
    main()
    

