FROM jenkins/inbound-agent:latest

USER root

# Update and install Python (both python3 and pip)
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set default python and pip if needed
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

USER jenkins