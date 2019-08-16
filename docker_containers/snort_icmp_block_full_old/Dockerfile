FROM ubuntu:xenial

ENV DAQ_VER=2.0.6 \
    SNORT_VER=2.9.12

# Install Dependencies
RUN apt-get update && \
    apt-get install -yqq build-essential autotools-dev bison flex gcc \
    	    	    	 libdumbnet-dev liblzma-dev libpcap-dev libpcre3-dev \
			 libssl-dev libluajit-5.1-dev pkg-config make  wget \
			 openssl zlib1g-dev libwlocate-dev cmake libtool \
			 autoconf libnetfilter-queue-dev libnghttp2-dev \
			 python

# Optional packages
RUN apt-get install -yqq cpputest libsqlite3-dev uuid-dev 

RUN mkdir -p ~/snort_src && \
    cd ~/snort_src

# Install additional dependencies
# -safec
RUN cd ~/snort_src && \
    wget https://downloads.sourceforge.net/project/safeclib/libsafec-10052013.tar.gz && \
    tar -xzvf libsafec-10052013.tar.gz && \
    cd libsafec-10052013/ && \
    ./configure && make && make install 

# -Ragel
RUN cd  ~/snort_src && \
    wget http://www.colm.net/files/ragel/ragel-6.10.tar.gz && \
    tar -xzvf ragel-6.10.tar.gz && \
    cd ragel-6.10/ && \
    ./configure && make && make install 

# -Boost C++
RUN cd ~/snort_src && \
    wget https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz && \
    tar -xvzf boost_1_65_1.tar.gz 

# -DAQ
RUN cd ~/snort_src && \
    wget https://www.snort.org/downloads/snort/daq-${DAQ_VER}.tar.gz && \
    tar -xvzf daq-${DAQ_VER}.tar.gz && \
    cd daq-${DAQ_VER} && \
    ./configure && make && make install 

# Update shared libraries cache
RUN ldconfig

# Install SNORT
RUN cd ~/snort_src && \
    wget https://www.snort.org/downloads/snort/snort-${SNORT_VER}.tar.gz && \
    tar -xvzf snort-${SNORT_VER}.tar.gz && \
    cd snort-${SNORT_VER} && \
    ./configure --enable-sourcefire && make && make install 

RUN ln -s /opt/snort/bin/snort /usr/sbin/snort

# Create Configuration & Log folders
RUN mkdir -p /etc/snort/ && mkdir -p /etc/snort/rules/ &&  \
    mkdir -p /var/log/snort/ && touch /etc/snort/snort.conf && \
    touch /etc/snort/rules/local.rules && touch /var/log/snort/alert \
    touch /etc/snort/threshold.conf && mkdir -p /usr/local/lib/snort_dynamicrules

RUN touch /etc/snort/rules/app-detect.rules && \
    touch /etc/snort/rules/attack-responses.rules && \
    touch /etc/snort/rules/backdoor.rules && \
    touch /etc/snort/rules/bad-traffic.rules && \
    touch /etc/snort/rules/blacklist.rules && \
    touch /etc/snort/rules/botnet-cnc.rules && \
    touch /etc/snort/rules/browser-chrome.rules && \
    touch /etc/snort/rules/browser-firefox.rules && \
    touch /etc/snort/rules/browser-ie.rules && \
    touch /etc/snort/rules/browser-other.rules && \
    touch /etc/snort/rules/browser-plugins.rules && \
    touch /etc/snort/rules/browser-webkit.rules && \
    touch /etc/snort/rules/chat.rules && \
    touch /etc/snort/rules/content-replace.rules && \
    touch /etc/snort/rules/ddos.rules && \
    touch /etc/snort/rules/dns.rules && \
    touch /etc/snort/rules/dos.rules && \
    touch /etc/snort/rules/experimental.rules && \
    touch /etc/snort/rules/exploit-kit.rules && \
    touch /etc/snort/rules/exploit.rules && \
    touch /etc/snort/rules/file-executable.rules && \
    touch /etc/snort/rules/file-flash.rules && \
    touch /etc/snort/rules/file-identify.rules && \
    touch /etc/snort/rules/file-image.rules && \
    touch /etc/snort/rules/file-java.rules && \
    touch /etc/snort/rules/file-multimedia.rules && \
    touch /etc/snort/rules/file-office.rules && \
    touch /etc/snort/rules/file-other.rules && \
    touch /etc/snort/rules/file-pdf.rules && \
    touch /etc/snort/rules/finger.rules && \
    touch /etc/snort/rules/ftp.rules && \
    touch /etc/snort/rules/icmp-info.rules && \
    touch /etc/snort/rules/icmp.rules && \
    touch /etc/snort/rules/imap.rules && \
    touch /etc/snort/rules/indicator-compromise.rules && \
    touch /etc/snort/rules/indicator-obfuscation.rules && \
    touch /etc/snort/rules/indicator-scan.rules && \
    touch /etc/snort/rules/indicator-shellcode.rules && \
    touch /etc/snort/rules/info.rules && \
    touch /etc/snort/rules/malware-backdoor.rules && \
    touch /etc/snort/rules/malware-cnc.rules && \
    touch /etc/snort/rules/malware-other.rules && \
    touch /etc/snort/rules/malware-tools.rules && \
    touch /etc/snort/rules/misc.rules && \
    touch /etc/snort/rules/multimedia.rules && \
    touch /etc/snort/rules/mysql.rules && \
    touch /etc/snort/rules/netbios.rules && \
    touch /etc/snort/rules/nntp.rules && \
    touch /etc/snort/rules/oracle.rules && \
    touch /etc/snort/rules/os-linux.rules && \
    touch /etc/snort/rules/os-mobile.rules && \
    touch /etc/snort/rules/os-other.rules && \
    touch /etc/snort/rules/os-solaris.rules && \
    touch /etc/snort/rules/os-windows.rules && \
    touch /etc/snort/rules/other-ids.rules && \
    touch /etc/snort/rules/p2p.rules && \
    touch /etc/snort/rules/phishing-spam.rules && \
    touch /etc/snort/rules/policy-multimedia.rules && \
    touch /etc/snort/rules/policy-other.rules && \
    touch /etc/snort/rules/policy.rules && \
    touch /etc/snort/rules/policy-social.rules && \
    touch /etc/snort/rules/policy-spam.rules && \
    touch /etc/snort/rules/pop2.rules && \
    touch /etc/snort/rules/pop3.rules && \
    touch /etc/snort/rules/protocol-dns.rules && \
    touch /etc/snort/rules/protocol-finger.rules && \
    touch /etc/snort/rules/protocol-ftp.rules && \
    touch /etc/snort/rules/protocol-icmp.rules && \
    touch /etc/snort/rules/protocol-imap.rules && \
    touch /etc/snort/rules/protocol-nntp.rules && \
    touch /etc/snort/rules/protocol-other.rules && \
    touch /etc/snort/rules/protocol-pop.rules && \
    touch /etc/snort/rules/protocol-rpc.rules && \
    touch /etc/snort/rules/protocol-scada.rules && \
    touch /etc/snort/rules/protocol-services.rules && \
    touch /etc/snort/rules/protocol-snmp.rules && \
    touch /etc/snort/rules/protocol-telnet.rules && \
    touch /etc/snort/rules/protocol-tftp.rules && \
    touch /etc/snort/rules/protocol-voip.rules && \
    touch /etc/snort/rules/pua-adware.rules && \
    touch /etc/snort/rules/pua-other.rules && \
    touch /etc/snort/rules/pua-p2p.rules && \
    touch /etc/snort/rules/pua-toolbars.rules && \
    touch /etc/snort/rules/rpc.rules && \
    touch /etc/snort/rules/rservices.rules && \
    touch /etc/snort/rules/scada.rules && \
    touch /etc/snort/rules/scan.rules && \
    touch /etc/snort/rules/server-apache.rules && \
    touch /etc/snort/rules/server-iis.rules && \
    touch /etc/snort/rules/server-mail.rules && \
    touch /etc/snort/rules/server-mssql.rules && \
    touch /etc/snort/rules/server-mysql.rules && \
    touch /etc/snort/rules/server-oracle.rules && \
    touch /etc/snort/rules/server-other.rules && \
    touch /etc/snort/rules/server-samba.rules && \
    touch /etc/snort/rules/server-webapp.rules && \
    touch /etc/snort/rules/shellcode.rules && \
    touch /etc/snort/rules/smtp.rules && \
    touch /etc/snort/rules/snmp.rules && \
    touch /etc/snort/rules/specific-threats.rules && \
    touch /etc/snort/rules/spyware-put.rules && \
    touch /etc/snort/rules/sql.rules && \
    touch /etc/snort/rules/telnet.rules && \
    touch /etc/snort/rules/tftp.rules && \
    touch /etc/snort/rules/virus.rules && \
    touch /etc/snort/rules/voip.rules && \
    touch /etc/snort/rules/web-activex.rules && \
    touch /etc/snort/rules/web-attacks.rules && \
    touch /etc/snort/rules/web-cgi.rules && \
    touch /etc/snort/rules/web-client.rules && \
    touch /etc/snort/rules/web-coldfusion.rules && \
    touch /etc/snort/rules/web-frontpage.rules && \
    touch /etc/snort/rules/web-iis.rules && \
    touch /etc/snort/rules/web-misc.rules && \
    touch /etc/snort/rules/web-php.rules && \
    touch /etc/snort/rules/x11.rules && \
    touch /etc/snort/rules/white_list.rules && \
    touch /etc/snort/rules/black_list.rules


COPY snort.conf /etc/snort/snort.conf 
COPY local.rules /etc/snort/rules/local.rules
COPY community.rules /etc/snort/rules/community.rules
COPY sid-msg.map /etc/snort/sid-msg.map
COPY classification.config /etc/snort/classification.config
COPY reference.config /etc/snort/reference.config
COPY unicode.map /etc/snort/unicode.map

COPY run.sh run.sh

CMD ["-Q", "--daq", "afpacket", "--daq-var", "buffer_size_mb=4", "-i", "eth0:eth1", "-c", "/etc/snort/snort.conf", "-l", "/var/log/snort/"]

ENTRYPOINT ["/run.sh"]
#ENTRYPOINT ["/idle.sh"]

