FROM python:3.6.4-alpine3.7
# docker build -t imap-2-http-connector -f docker/Dockerfile .

COPY lib/* /opt/app/lib/
COPY src/main/python/*.py /opt/app/src/
COPY src/main/resources/* /opt/app/
COPY docker/scripts/tini-static-amd64 /usr/local/bin/tini
COPY docker/scripts/docker-entrypoint.sh /docker-entrypoint.sh

RUN /usr/local/bin/python --version
RUN chown -R nobody:nobody /opt/app/ && chmod +x /usr/local/bin/tini && chmod +x /docker-entrypoint.sh \
    && ls -al /opt/app/src && ls -al /opt/app/ \
    && ls -al /opt/app/lib && pip install /opt/app/lib/*.whl && rm -f /opt/app/lib/* && ls -al /opt/app/lib

USER nobody
WORKDIR /opt/app
ENTRYPOINT ["/usr/local/bin/tini", "--", "/docker-entrypoint.sh"]