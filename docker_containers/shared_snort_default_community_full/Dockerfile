FROM ubuntu:xenial

RUN ldconfig

COPY local.rules /etc/snort/rules/local.rules

COPY run.sh run.sh

# Create Configuration & Log folders
RUN mkdir -p /etc/snort/ && \
    mkdir -p /var/log/snort/ && \
    touch /var/log/snort/alert

# Install Dependencies
RUN apt-get update && \	
    apt-get install -yqq build-essential autotools-dev bison flex gcc \
    	    	    	 libdumbnet-dev liblzma-dev libpcap-dev libpcre3-dev \
			 libssl-dev libluajit-5.1-dev pkg-config make  wget \
			 openssl zlib1g-dev libwlocate-dev cmake libtool \
			 autoconf libnetfilter-queue-dev libnghttp2-dev \
			 python iperf psmisc

RUN apt-get install -yqq less

ENTRYPOINT ["/run.sh"]

