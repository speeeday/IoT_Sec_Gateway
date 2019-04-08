
import sys

def pss(e):
    return e['Pss:']

def private(e):
    return e['Private_Clean:'] + e['Private_Dirty:']

def shared(e):
    return e['Pss:'] - e['Private_Clean:'] - e['Private_Dirty:']


if len(sys.argv) < 2:
    print "Usage: ./read_smaps.py <# instances>"
    sys.exit()

base_filename = 'sharedsingle1mb/smaps_snort'

if len(sys.argv) < 3:
    print "Usage: " + sys.argv[0] + " <# instances> [pss|private|shared]"
    sys.exit()
elif sys.argv[2] == 'pss':
    mem_fn = pss
elif sys.argv[2] == 'private':
    mem_fn = private
elif sys.argv[2] == 'shared':
    mem_fn = shared
else:
    print "Usage: " + sys.argv[0] + " <# instances> [pss|private|shared]"
    sys.exit()

num_instances = int(sys.argv[1])


libs = ['/lib/arm-linux-gnueabihf/ld-2.23.so', # Linker library
        '/lib/arm-linux-gnueabihf/libnss_files-2.23.so', # libnss (libc related)
        '/usr/lib/arm-linux-gnueabihf/libnghttp2.so.14.4.1',
        '/lib/arm-linux-gnueabihf/libpcre.so.3.13.2',
        '/lib/arm-linux-gnueabihf/libm-2.23.so',
        '/lib/arm-linux-gnueabihf/libcrypto.so.1.0.0',
        '/lib/arm-linux-gnueabihf/libdl-2.23.so',
        '/usr/lib/arm-linux-gnueabihf/libnetfilter_queue.so.1.3.0',
        '/usr/local/lib/libsfbpf.so.0.0.1',
        '/usr/lib/arm-linux-gnueabihf/libpcap.so.1.7.4',
        '/usr/lib/arm-linux-gnueabihf/libdumbnet.so.1.0.1',
        '/lib/arm-linux-gnueabihf/libz.so.1.2.8',
        '/lib/arm-linux-gnueabihf/liblzma.so.5.0.0',
        '/lib/arm-linux-gnueabihf/libpthread-2.23.so',
        '/lib/arm-linux-gnueabihf/libc-2.23.so',
        '/usr/lib/arm-linux-gnueabihf/libnfnetlink.so.0.2.0',
        '/lib/arm-linux-gnueabihf/libmnl.so.0.1.0',

        '/usr/lib/arm-linux-gnueabihf/libluajit-5.1.so.2.0.4', # community rules
        '/lib/arm-linux-gnueabihf/libgcc_s.so.1', # community rules

        '/lib/arm-linux-gnueabihf/libnsl-2.23.so',
        '/lib/arm-linux-gnueabihf/libtinfo.so.5.9',
        '/lib/arm-linux-gnueabihf/libnss_compat-2.23.so',
        '/lib/arm-linux-gnueabihf/libnss_nis-2.23.so',
        
        '/bin/bash'
        
]


unk_cnt = 1

di = []

for i in range(num_instances):
    di.append({})

for i in range(num_instances):
    d = di[i]

    cf = ''
    cp = ''



    filename = base_filename + '_' + str(num_instances) + '_' + str(i+1) + '.txt'
    f = open(filename, 'r')

    for l in f.readlines():
        # New Entry
        if '-' in l:
            ll = l.split()
            if ll[-1] == '0':
                ll.append('Unknown #%d' % unk_cnt)
                unk_cnt += 1
            if ll[-1] not in d:
                d[ll[-1]] = {}
            cf = ll[-1]
            cp = ll[1]
            d[ll[-1]][ll[1]] = {}
        # Attribute
        elif 'VmFlags' in l:
            k=0
        else:
            dd = d[cf][cp]
            ll = l.split()
            if ll[-1] != 'kB':
                print "Different metric"
                print l
                print dd
                print ll
                sys.exit()
            dd[ll[0]] = int(ll[1])



# All Process Memory
lib_s = 0
socket_s = 0
unk_s = 0
stack_s = 0
vvar_s = 0
vdso_s = 0
sigpage_s = 0
heap_s = 0
vectors_s = 0
snort_s = 0


for i in range(num_instances):
    d = di[i]
    for k in d:
        for p in d[k]:
            if k in libs:
                lib_s += mem_fn(d[k][p])
            elif 'snort' in k:
                snort_s += mem_fn(d[k][p])
            elif 'Unknown' in k:
                unk_s += mem_fn(d[k][p])
            elif 'socket' in k:
                socket_s += mem_fn(d[k][p])
            elif 'stack' in k:
                stack_s += mem_fn(d[k][p])
            elif 'vvar' in k:
                vvar_s += mem_fn(d[k][p])
            elif 'vdso' in k:
                vdso_s += mem_fn(d[k][p])
            elif 'sigpage' in k:
                sigpage_s += mem_fn(d[k][p])
            elif 'heap' in k:
                heap_s += mem_fn(d[k][p])
            elif 'vectors' in k:
                vectors_s += mem_fn(d[k][p])
            else:
                print "Unknown! : " + k
                sys.exit()


print "%d" % heap_s
print "%d" % lib_s
print "%d" % sigpage_s
print "%d" % snort_s
print "%d" % socket_s
print "%d" % stack_s
print "%d" % unk_s
print "%d" % vdso_s
print "%d" % vectors_s
print "%d" % vvar_s


#print "snort: %d kB" % snort_s
#print "libraries: %d kB" % lib_s
#print "sockets: %d kB" % socket_s
#print "unknown: %d kB" % unk_s
#print "stack: %d kB" % stack_s
#print "vvar: %d kB" % vvar_s
#print "vdso: %d kB" % vdso_s
#print "sigpage: %d kB" % sigpage_s
#print "heap: %d kB" % heap_s
#print "vectors: %d kB" % vectors_s
