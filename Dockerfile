FROM docker.io/library/python:3.10-alpine

# Add Tini
#ENV TINI_VERSION v0.19.0
#ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
#RUN chmod +x /tini
#ENTRYPOINT ["/tini", "--"]

COPY app /app

WORKDIR /app

RUN 	pip install pipenv && \
			pipenv requirements > requirements && \
			pip install -r /app/requirements

# Run your program under Tini
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
