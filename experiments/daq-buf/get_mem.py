#! /usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib.cm as cm
import argparse
import sys

def parse_entry(r):
    d = {}
    # get each attribute
    attrs = r.strip('\x00').split('\x00')
    for a in attrs:
        if a[0] == 'p':
            d['process ID'] = int(a[1:])
        elif a[0] == 'g':
            d['process group ID'] = int(a[1:])
        elif a[0] == 'R':
            d['parent process ID'] = int(a[1:])
        elif a[0] == 'c':
            d['process command name'] = str(a[1:])
        elif a[0] == 'u':
            d['process user ID'] = int(a[1:])
        elif a[0] == 'L':
            d['process login name'] = str(a[1:])
        elif a[0] == 'f':
            d['file descriptor'] = str(a[1:])
        elif a[0] == 'a':
            d['file access mode'] = str(a[1:])
        elif a[0] == 'l':
            d['file\'s lock status'] = str(a[1:])
        elif a[0] == 't':
            d['file\'s type'] = str(a[1:])
        elif a[0] == 'D':
            d['file\'s major/minor device number'] = str(a[1:])
        elif a[0] == 's':
            d['file\'s size'] = int(a[1:])
        elif a[0] == 'i':
            d['file\'s inode number'] = int(a[1:])
        elif a[0] == 'k':
            d['link count'] = str(a[1:])
        elif a[0] == 'n':
            d['file name, comment, Internet address'] = str(a[1:])
        elif a[0] == 'G':
            d['file flaGs'] = str(a[1:])
        elif a[0] == 'o':
            d['file\'s offset'] = str(a[1:])
        elif a[0] == 'd':
            d['file\'s device character code'] = str(a[1:])
        elif a[0] == 'K':
            d['tasK ID'] = int(a[1:])
        elif a[0] == 'P':
            d['protocol name'] = str(a[1:])
        elif a[0] == 'T':
            d['TCP/TCPI info'] = str(a[1:])
        elif a[0] == '':
            d[''] = str(a[1:])
        elif a[0] == '':
            d[''] = str(a[1:])
        elif a[0] == '':
            d[''] = str(a[1:])
        elif a[0] == '':
            d[''] = str(a[1:])
        elif a[0] == '':
            d[''] = str(a[1:])
        else:
            print "Received Unknown Prefix Character '%c' with value '%s'" % (a[0], str(a[1:]))
            sys.exit()
    return d

def parse_meminfo_entry(r):
    d = {}
    # get each attribute
    attrs = r.strip('\n').split('\n')
    for a in attrs:
        if ':' not in a:
            continue
        aa = a.split(':')
        d[aa[0]] = aa[1].strip(' ')
    return d
        
def get_meminfo_b(a):
    ms = []
    for d in a:
#        print d
        memtotal = 0
        memfree = 0
        swaptotal = 0
        swapfree = 0
        if d == {}:
            continue
        if d['MemTotal'][-2:] == 'kB':
            memtotal = int(d['MemTotal'][:-3])
        else:
            print "PROBLEM"
            sys.exit()
        if d['MemFree'][-2:] == 'kB':
            memfree = int(d['MemFree'][:-3])
        else:
            print "PROBLEM"
            sys.exit()
        if d['SwapTotal'][-2:] == 'kB':
            swaptotal = int(d['SwapTotal'][:-3])
        else:
            print "PROBLEM"
            sys.exit()
        if d['SwapFree'][-2:] == 'kB':
            swapfree = int(d['SwapFree'][:-3])
        else:
            print "PROBLEM"
            sys.exit()
        print memtotal, memfree, swaptotal, swapfree
        ms.append(swaptotal + memtotal - memfree - swapfree)
    return ms

def get_mem_b(os):
    ms = []
    for ds in os:
        m = 0
        for d in ds:
            if 'file\'s size' in d:
                m += d['file\'s size']
        ms.append(m)
    return ms

def get_mem_kb(os):
    ms = []
    for ds in os:
        m = 0
        for d in ds:
            if 'file\'s size' in d:
                m += d['file\'s size']
        ms.append(m / (1 << 10))
    return ms

def get_mem_mb(os):
    ms = []
    for ds in os:
        m = 0
        for d in ds:
            if 'file\'s size' in d:
                m += d['file\'s size']
        ms.append(m / (1 << 20))
    return ms

def get_mem_gb(os):
    ms = []
    for ds in os:
        m = 0
        for d in ds:
            if 'file\'s size' in d:
                m += d['file\'s size']
        ms.append(m / (1 << 30))
    return ms


if __name__ == "__main__":



    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Input file")
    parser.add_argument("-o", "--out", type=str, default="mountain.png", help="Output file")
    #parser.add_argument('--instances', '-n', required=True, type=int)

    args = parser.parse_args()

    output = open(args.file, 'r').read()
    x = []
    y = []

    
    # split lsof output at each timestep
    times_output = output.strip('==========').split('==========')
    parsed_output = []
    
    for t in range(0, len(times_output)):
        curr_entry = times_output[t]
        parsed_entry = parse_meminfo_entry(curr_entry)
        parsed_output.append(parsed_entry)

    # do some kind of processing on the entries, to get x,y's

    instances = 30
    
    x = range(instances+1)
    # skip first 2 parsed entries, were for stabilizing
    #y = get_mem_b(parsed_output[2:])
    y = get_meminfo_b(parsed_output[2:])


    init = True
    v = 0
    for yy in y:
        if init:
            init = False
            v = yy
        else:
            init = True
            print v-yy
    
    # process data into x,y: attributes to graph
    # x, y, z = numpy.loadtxt(args.file, unpack=True)

    #print len(x)
    #print len(y)

    #plt.plot(x, y)
    #plt.plot(x, y, 'bo')
    
    #plt.xlabel('# Snort Instances')
    #plt.ylabel('Memory (Kilobytes)')

    #plt.savefig('instances%d_vs_memory.png' % instances)

    
    #sys.exit()

    
