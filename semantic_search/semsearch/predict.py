import base64
import os
from io import BytesIO

from PIL import Image
from semsearch.encoding import clip_encoding
from semsearch.load import load_corpus, load_model
from semsearch.retrieval import search

corpus = load_corpus()
model = load_model()


def make_predictions(input_data):
    query_text = input_data
    query_embed = clip_encoding.get_text_embeddings(query_text)
    query = {"query_text": query_text, "query_embed": query_embed}
    hits = search.cosine_search(query, corpus, k=3)
    for h in hits:
        # Currently this returns the image as uri
        # If the images are available online, this can be changed to url
        name = corpus['img_names'][h['corpus_id']]
        img = Image.open(name)
        data = BytesIO()
        img.save(data, "JPEG")
        data64 = base64.b64encode(data.getvalue())
        h['src'] = u'data:img/jpeg;base64,'+data64.decode('utf-8')
        h['alt'] = round(h['score'], 2)
        h['name'] = os.path.basename(name)
    return hits
