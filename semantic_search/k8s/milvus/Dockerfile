FROM python:3.7.14-slim-buster

RUN mkdir -p /opt/app
COPY ml_api_milvus /opt/app/ml_api_milvus
COPY ml_api_milvus/Makefile /opt/app/Makefile

RUN pip install --upgrade pip

# ensure we can run the make commands
RUN apt-get update -y && \
 	apt-get install -y make && \
 	apt-get install -y libffi-dev gcc && \
 	# for swagger
 	apt-get install -y curl

RUN pip install -r /opt/app/ml_api_milvus/requirements.in

ENV PYTHONPATH "${PYTHONPATH}:/opt/app/ml_api_milvus"
WORKDIR /opt/app

# run the flask app
CMD make "run-service-development"
#CMD ls