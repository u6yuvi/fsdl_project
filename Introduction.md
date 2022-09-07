# Local Development Setup

1. Install miniconda
2. Use environment.yml file for creating new environment in conda 

```
make conda-update
```

3. Install additional python packages in the newly created conda environment using pip-tools

```
make pip-tools
```

# Running Inference

1. Refer Package-Access jupyter notebook for running inference.

# Running Flask Server
1. Run ml_api/run.py to start the Flask Server.
2. Goto http://localhost:5000/ui/.
3. Goto POST /v1/predictions endpoint.
4. Click on Try Now and enter text under the section "Text query to match an image"
    For eg. Type "Running dogs" and hit execute.
5.   Response will be generated under the Response Body section below.

## Response

#corpus_id - Pointing to Image Index Number in the preseeded Image Corpus/
#Score - Cosine Similarity
#version - Model version

{
  "errors": [],
  "predictions": [
    {
      "corpus_id": 2,
      "score": 0.237429678440094
    },
    {
      "corpus_id": 3,
      "score": 0.23457613587379456
    },
    {
      "corpus_id": 0,
      "score": 0.19539634883403778
    }
  ],
  "version": "0.1.0"
}


# Docker Setup[In-Progress]

## Run the application manually 
  1.  Build Docker Container

```
sudo docker build -f docker/Dockerfile  -t fsdl .
```

  2. Run docker container[bash]

``` 
sudo docker run -it -p 5000:5000 fsdl bash
```
  3. Run the flask app

```
python3 ml_api/run.py
```
  4. Goto http://localhost:5000/ui/

## Run Using Docker Compose

  1. Build and Run Docker
```
sudo docker-compose -f docker/docker-compose.yml up -d --build
```

  2. Goto http://localhost:5000/ui/

