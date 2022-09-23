import os
import zipfile

from sentence_transformers import util
from tqdm.autonotebook import tqdm

# Next, we get about 25k images from Unsplash
img_folder = "./data/photos/"
if not os.path.exists(img_folder) or len(os.listdir(img_folder)) == 0:
    os.makedirs(img_folder, exist_ok=True)

    photo_filename = "unsplash-25k-photos.zip"
    if not os.path.exists(photo_filename):  # Download dataset if does not exist
        util.http_get("http://sbert.net/datasets/" + photo_filename, photo_filename)

    # Extract all images
    with zipfile.ZipFile(photo_filename, "r") as zf:
        for member in tqdm(zf.infolist(), desc="Extracting"):
            zf.extract(member, img_folder)
