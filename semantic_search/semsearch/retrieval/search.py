from sentence_transformers import util


# Next, we define a search function.
def cosine_search(query, corpus, k=3):

    # Then, we use the util.semantic_search function, which computes
    # the cosine-similarity
    # between the query embedding and all image embeddings.
    # It then returns the top_k highest ranked images, which we output
    hits = util.semantic_search(
        query["query_embed"], corpus["embeddings"], top_k=k
    )[0]

    return hits
