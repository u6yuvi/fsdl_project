import glob
from pathlib import Path

from semsearch.config import config
from semsearch.encoding import clip_encoding
from semsearch.models import load_clip_model
from sentence_transformers import SentenceTransformer

config.DATASET_DIR


def load_corpus():
    img_names = list(glob.glob(str(config.DATASET_DIR) + "/*.jpg"))
    print("Images:", len(img_names))
    embeddings = clip_encoding.get_image_embeddings(img_names[:20])
    corpus = {"embeddings": embeddings, "img_names": img_names[:20]}
    return corpus


def load_model():
    # img_model = SentenceTransformer('clip-ViT-B-32')
    model = load_clip_model()
    return model
