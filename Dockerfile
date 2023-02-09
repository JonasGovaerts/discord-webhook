FROM docker.io/library/python:3.10-alpine

COPY app /app

WORKDIR /app

RUN 	pip install pipenv && \
			pipenv requirements > requirements && \
			pip install -r /app/requirements

# Run your program under Tini
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

ARG S6_OVERLAY_VERSION=3.1.3.0
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
ENTRYPOINT ["/init"]
