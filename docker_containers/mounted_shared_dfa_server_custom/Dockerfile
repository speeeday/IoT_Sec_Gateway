FROM ubuntu:xenial

ENV DAQ_VER=2.0.6 \
    SNORT_VER=2.9.12

RUN ldconfig

# Install Dependencies
RUN apt-get update && \
    apt-get install -yqq build-essential autotools-dev bison flex gcc \
    	    	    	 libdumbnet-dev liblzma-dev libpcap-dev libpcre3-dev \
			 libssl-dev libluajit-5.1-dev pkg-config make  wget \
			 openssl zlib1g-dev libwlocate-dev cmake libtool \
			 autoconf libnetfilter-queue-dev libnghttp2-dev \
			 python iperf

# Optional packages
RUN apt-get install -yqq cpputest libsqlite3-dev uuid-dev 

# Create Configuration & Log folders
RUN mkdir -p /etc/snort/ && \
    mkdir -p /var/log/snort/ && \
    touch /var/log/snort/alert

RUN apt-get update && \
    apt-get install -yqq ethtool net-tools iputils-ping tcpdump iptables psutils psmisc iperf3 less vim

COPY run.sh run.sh

CMD ["-Q", "--daq", "afpacket", "--daq-var", "buffer_size_mb=1", "-i", "eth0:eth2", "-c", "/testvolume/linux-rules/etc/snort.conf", "-l", "/var/log/snort/"]
#CMD ["-Q", "--daq", "afpacket", "-i", "eth0:eth2", "-c", "/testvolume/linux-rules/etc/snort.conf", "-l", "/var/log/snort/"]

ENTRYPOINT ["/run.sh"]
#ENTRYPOINT ["/idle.sh"]

