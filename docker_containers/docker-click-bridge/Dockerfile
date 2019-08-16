FROM click:latest

COPY bridge.click bridge.click
COPY run.sh run.sh

# Run bridge application
CMD ["eth1", "eth2"]
ENTRYPOINT ["/run.sh"]

