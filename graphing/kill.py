#!/usr/bin/env python

import argparse
import shlex
import subprocess

BRIDGE = 'br0'

def docker_killall(name):
    cmd='/usr/bin/sudo /usr/bin/docker kill {}'
    cmd=cmd.format(name)
    subprocess.call(shlex.split(cmd))

def lsof_killall(name):
    cmd='/usr/bin/sudo /usr/bin/killall lsof'
    subprocess.call(shlex.split(cmd))

    
def main():
    parser=argparse.ArgumentParser(description='Clean up containers and switch ports after experiment')
    parser.add_argument('--number', '-n', required=True, type=int)
    args=parser.parse_args()
    #name_list=['test{}'.format(i) for i in range(args.number)]
    for i in range(args.number):
        name='test{}'.format(i)
        docker_killall(name)

if __name__=='__main__':
    main()

