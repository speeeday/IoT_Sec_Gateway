FROM ubuntu:xenial

RUN ldconfig

COPY run.sh run.sh

COPY local.rules /etc/snort/rules/local.rules

ENTRYPOINT ["/run.sh"]

