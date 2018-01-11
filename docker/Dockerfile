FROM python:3.5-alpine
# docker build -t imap-2-http-connector -f docker/Dockerfile .

COPY src/main/python/*.py /opt/app/src/
#COPY src/main/resources/* /opt/app/
COPY docker/resources/tini-static-amd64 /usr/local/bin/tini
COPY docker/resources/docker-entrypoint.sh /docker-entrypoint.sh
COPY docker/resources/key.pem /opt/app/key.pem

RUN chown -R nobody:nobody /opt/app/ && chmod +x /usr/local/bin/tini && chmod +x /docker-entrypoint.sh

USER nobody
WORKDIR /opt/app
ENTRYPOINT ["/usr/local/bin/tini", "--", "/docker-entrypoint.sh"]