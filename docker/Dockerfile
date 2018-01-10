FROM python:3.5-alpine
# docker build -t imap-2-http-connector -f docker/Dockerfile .

RUN mkdir -p /opt/app/src
COPY src/main/python/*.py /opt/app/src/
#COPY src/main/resources/* /opt/app/

#COPY src/requirements.txt /tmp/requirements.txt
#RUN pip install -r requirements.txt

WORKDIR /opt/app
ENTRYPOINT ["/usr/local/bin/python", "-u", "/opt/app/src/main.py"]
CMD ["/config.cfg"]
