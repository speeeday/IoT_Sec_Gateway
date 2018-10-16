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
            d['link count'] = int(a[1:])
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

if __name__ == "__main__":



    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Input file")
    parser.add_argument("-o", "--out", type=str, default="mountain.png", help="Output file")
    args = parser.parse_args()

    output = open(args.file, 'r').read()

    # split lsof output at each timestep
    times_output = output.strip('\nm\x00\n').split('\nm\x00\n')
    
    
    for t in range(0, len(times_output)):
        curr_entries = times_output[t].strip('\n').split('\n')
        parsed_entries = []
        if t != 0 and len(curr_entries) != prev:
            print "Differed by %d, Prev: %d, Curr %d" % ((len(curr_entries)-prev), prev, len(curr_entries))
            #sys.exit()
        prev = len(curr_entries)
        for i in range(0, len(curr_entries)):
            raw_entry = curr_entries[i]
            parsed_entry = parse_entry(raw_entry)
            parsed_entries.append(parsed_entry)

    # do some kind of processing on the entries, to get x,y's

            
    # process data into x,y: attributes to graph
    # x, y, z = numpy.loadtxt(args.file, unpack=True)
            
    sys.exit()

    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.invert_yaxis();
    ax.set_xlabel("Stride")
    ax.set_ylabel("log2(size) (Bytes)")
    ax.set_zlabel("MB/s")
    plt.tight_layout()

    ax.plot_trisurf(x, y, z, cmap=cm.Blues_r)
    plt.savefig(args.out)

    
