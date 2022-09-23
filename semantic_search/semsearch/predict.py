from semsearch.encoding import clip_encoding
from semsearch.retrieval import search
from semsearch.load import load_corpus,load_model


corpus = load_corpus()
model = load_model()


def make_predictions(input_data):
    query_text = input_data
    query_embed = clip_encoding.get_text_embeddings(query_text)
    query = {"query_text":query_text,"query_embed":query_embed}
    hits = search.cosine_search(query,corpus,k=3)
    return hits
