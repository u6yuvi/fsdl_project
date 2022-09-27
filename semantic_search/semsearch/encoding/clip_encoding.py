# First, we load the respective CLIP model
import numpy as np
from PIL import Image

from ..models import load_clip_model

# model = SentenceTransformer('clip-ViT-B-32')
model = load_clip_model()


# First, we encode the query (which can either be an image or a text string)
def get_text_embeddings(query):
    query_emb = model.encode(
        [query], convert_to_tensor=True, show_progress_bar=False)
    query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)
    return query_emb


def get_image_embeddings(img_names):
    print("Images:", len(img_names))

    # non-multilingual CLIP Model
    img_emb = model.encode(
        [Image.open(filepath) for filepath in img_names],
        batch_size=128,
        convert_to_tensor=True,
        show_progress_bar=True,
    )
    img_emb = img_emb / np.linalg.norm(img_emb, axis=1, keepdims=True)
    return img_emb
