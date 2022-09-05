# FSDL 2022 Project

## Tasks
1. Extracting Text/Image Embeddings using Pre-trained CLIP Model.
2. Perform approximate similarity matching to find items similar to a given item during inference on Vector 3. Database.[Milvus]
4. Use of ML Inference Server preferably Nvidia Triton Inference Server.
5. Use of REST API/gRPC service, handling natural language queries/images and matching them against relevant images.
6. Building Inference Data Pipeline using Language Wrappers.
7. Monitoring Metrics 
8. Monitoring Logs 


# Project Proposal

https://docs.google.com/document/d/1AUioMU8E8C5zYtmUH28Hc1yxMGzxbE4kJCtmRKNUvco/edit?usp=sharing


Refer Introduction page for environemnt setup and code exectution.

## Current Progress

1. Integrated Clip Model from Sentence Trasnformer.
2. Preseeding of Images in memory for Similarity Search.
3. Use of REST API to do Text Search on a preseeded Image corpus.

## TODO

1. Explore and Integrate Prometheus and Grafana for Monitoring.
2. Integrate Milvus for Preseeding the Image Corpus in the Vector Database to do approximate nearest neighbour search.
3. Use of AWS instance to reproduce the exisiting pipeline.
4. Explore Amazon S3 Object store to fetch Image Corpus for Preseeding in the Vector Database.
5. Adding REST API endpoint for Image to Image Search.