# Official Ubuntu 16.04 image
FROM ubuntu:xenial

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
	build-essential \
	git \
	autoconf \
	install-info \
	libpcap0.8-dev \
	libpcap0.8-dbg \
	ethtool \
	python \
	iperf \
	&& apt-get clean

# Build and install click
RUN git clone https://github.com/kohler/click.git \
	&& cd click \
	&& ./configure --disable-linuxmodule \
	&& make \
	&& make install

# Run test config
CMD ["/click/conf/test.click"]
ENTRYPOINT ["/usr/local/bin/click"]

