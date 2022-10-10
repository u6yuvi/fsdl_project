FROM python:3.9.5-slim-buster

RUN mkdir -p /opt/app
#COPY ml_api/requirements.txt /opt/app/requirements.txt
COPY ml_api /opt/app/ml_api
COPY semsearch_pkg/semsearch /opt/app/semsearch
COPY docker /opt/app/docker
# COPY run.py /opt/app/run.py
#COPY . /opt/app
RUN pip install --upgrade pip

# ensure we can run the make commands
RUN apt-get update -y && \
 	apt-get install -y make && \
 	apt-get install -y libffi-dev gcc && \
 	# for swagger
 	apt-get install -y curl

RUN pip install -r /opt/app/ml_api/requirements.txt
COPY ml_api/Makefile /opt/app/Makefile
# COPY api /opt/app/api
# COPY run.py /opt/app/run.py
#COPY semsearch /opt/app/semsearch
ENV PYTHONPATH "${PYTHONPATH}:/opt/app/semsearch"
WORKDIR /opt/app

# run the flask app
CMD make "run-service-development"
#CMD ls