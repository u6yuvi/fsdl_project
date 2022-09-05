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

# Docker Setup[In-Progress]
# Build Docker Container

```
sudo docker build -f docker/Dockerfile  -t fsdl .
```

## Mount semsearch_pkg as volume

``` 
sudo docker run -it -v $(pwd):/opt/app -p 8888:8888 fsdl bash
```

# Running Inference

1. Refer Package-Access jupyter notebook for running inference.


