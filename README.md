# FSDL 2022 Project

## Tasks
1. Extracting Text/Image Embeddings using Pre-trained CLIP Model.
2. Perform approximate similarity matching to find items similar to a given item during inference on Vector 3. Database.[Milvus]
4. Use of ML Inference Server preferably Nvidia Triton Inference Serverp[Optional].
5. Use of REST API service, handling natural language queries/images and matching them against relevant images.
6. Building Inference Data Pipeline using Language Wrappers.
7. Monitoring Metrics with Prometheus.
8. Monitoring Logs with Kibana.


# Project Proposal

https://docs.google.com/document/d/1AUioMU8E8C5zYtmUH28Hc1yxMGzxbE4kJCtmRKNUvco/edit?usp=sharing


Refer ```Introduction.md``` page for environment setup and details about running the project in your system.

## Current Progress

- [x] Integrated Clip Model from Sentence Trasnformer.

- [x] Preseeding of Images in memory for Similarity Search.

- [x] Use of Swagger and Flask REST API to do Text Search on a preseeded Image corpus.
- [x] Docker Container to run the model inference.
- [x] Use of Docker Compose to create and run multiple containers.
- [x] Prometheus Integration for Monitoring Metrics.
- [x] Grafana Dashboard for Visualising the Monitoring Metrics.

## TODO

1. Integrate Milvus for Preseeding the Image Corpus in the Vector Database to do approximate nearest neighbour search.
3. Use of AWS instance to reproduce the exisiting pipeline.
4. Explore Amazon S3 Object store to fetch Image Corpus for Preseeding in the Vector Database.
5. Adding REST API endpoint for Image to Image Search.
6. Monitoring Logs with Kibana.
7. Adding precommit for code sanity checks.