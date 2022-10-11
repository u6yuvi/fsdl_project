import functools
import json
import os
import pathlib
import shutil
import tarfile
from pathlib import Path

import click
import pandas as pd
import redis
import requests
from redis.commands.json.path import Path as redPath
from tqdm import tqdm
from collections import OrderedDict


data_dir = Path('semantic_search/data/abo/')

url = 'https://amazon-berkeley-objects.s3.amazonaws.com/archives/'
filename = 'abo-images-small.tar'
tar_filename = os.path.join('abo', filename)
path = pathlib.Path('abo') / filename
listings = 'https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-listings.tar'
path_list = pathlib.Path('abo') / 'abo-listings.tar'
listings_dir = data_dir/ 'listings'/'metadata'
csv = data_dir / 'images' /'metadata'/'images.csv.gz'


r = redis.Redis(host="localhost", port=6379)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup, context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
def download():
    """Downloads the Amazon-Berkley Objects dataset to 'abo' directory and continues"""
    response = requests.get(url+filename, stream=True)
    if response.status_code != 200:
            response.raise_for_status()  # Will only raise for 4xx codes, so...
            raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(response.headers.get('Content-Length', 0))

    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    response.raw.read = functools.partial(response.raw.read)

    click.echo('-'*10 + " Downloading Image Data " + '-'*10)
    with tqdm.wrapattr(response.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)


    response2 = requests.get(listings, stream=True)
    if response2.status_code != 200:
        response2.raise_for_status()
        raise RuntimeError(f"Request to {listings} returned status code {r.status_code}")
    file_size = int(response2.headers.get('Content-Length', 0))
    response2.raw.read = functools.partial(response2.raw.read)

    click.echo('-'*10 + " Downloading Listing Data " + '-'*10)
    with tqdm.wrapattr(response2.raw, "read", total=file_size, desc=desc) as r_list:
        with path_list.open("wb") as f:
            shutil.copyfileobj(r_list, f)
    _extract()


@cli.command(name='extract')
def extract():
    "Untars the ABO dataset from 'abo' directory and continues"
    _extract()

def _extract():
    click.echo('-'*10 + " Extracting Data " + '-'*10)
    with tarfile.open(name=path) as tar:
        # Go over each member
        for member in tqdm(iterable=tar.getmembers(), total=len(tar.getmembers())):
            # Extract member
            tar.extract(member=member, path='abo')
    with tarfile.open(name=path_list) as tar:
        tar.extractall(path='abo')

    click.echo('-'*10 + " Data available at abo/ " + '-'*10)
    _add()


@cli.command()
def add():
    """Adds the untared metadata to redis db. Ensure redis is running.
    The image metadata is with `IMG:image_id` key.
    The photo (flat file) name to image_id mapping is with `MAP:name` key
    """
    _add()

def _add():
    listing_jsons = [f for f in listings_dir.iterdir()]
    def extract_values(x):
        if isinstance(x, list) and 'value' in x[0]:
            return [a['value'] for a in x]
        if pd.isna(x):
            return ''
        else:
            return x


    descriptors = ['item_id', 'item_name', 'model_name', 'brand', 'bullet_point']
    for listing_file in listing_jsons:
        df_list = pd.read_json(listing_file, lines=True)
        pipe = r.pipeline()
        for _, row in df_list.iterrows():
            feature = json.dumps({d: extract_values(row[d]) for d in descriptors})
            if not pd.isna(row['main_image_id']):
                key = "IMG:" + row['main_image_id']
                pipe.json().set(key, redPath.root_path(), feature)

            try:
                for img in row['other_image_id']:
                    key = "IMG:" + img
                    pipe.json().set(key, redPath.root_path(), feature)

            except TypeError:
                # ignore nans
                pass
        print("Starting to update redis")
        pipe.execute()

    df = pd.read_csv(csv)
    df['name'] = df['path'].str.extract(r'\/(.*).jpg')
    pipe = r.pipeline()
    for _, (name, id) in df[['name', 'image_id']].iterrows():
        pipe.set('MAP:'+ str(name), id )
    pipe.execute()


if __name__ == "__main__":
    cli()