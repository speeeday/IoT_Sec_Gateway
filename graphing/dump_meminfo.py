import time

start_time = int(time.time())
i = 0
interval = int(os.sys.argv[0])
outfile = str(os.sys.argv[1])
while True:
    while int(time.time()) <= ((start_time + i*interval)):
        time.sleep(1)
    os.system('sudo cat /proc/meminfo >> %s' % outfile)
    os.system('sudo echo "==========" >> %s' % outfile)
    i += 1
