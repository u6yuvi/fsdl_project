# Listing Information

### Make sure Redis is running

```bash
 sudo docker-compose -f docker/docker-compose.yml up -d
 ```

 ### Download and populate data

 Note that downloading data takes time, so the sequence is broken down to steps.

 ```shell
  python semantic_search/data/download_data.py --help
```
```text
Usage: download_data.py [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  download  Downloads the Amazon-Berkley Objects dataset to 'abo' directory
            and continues
  extract   Untars the ABO dataset from 'abo' directory and continues
  add       Adds the untared metadata to redis db. Ensure redis is running.
            The image metadata is with `IMG:image_id` key.
            The photo (flat file) name to image_id mapping
            is with `MAP:name` key
 ```