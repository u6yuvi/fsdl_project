from sentence_transformers import SentenceTransformer

# img_model = SentenceTransformer('clip-ViT-B-32')
# img_names = list(glob.glob('./data/photos/*.jpg'))

# def clip_embeddings(img_names = None):
#     print("Images:", len(img_names))

#     #non-multilingual CLIP Model
#     img_emb = img_model.encode([
#           Image.open(filepath)
#           for filepath in img_names[:10]
#       ], batch_size=128, convert_to_tensor=True, show_progress_bar=True)
#     img_emb = img_emb /  np.linalg.norm(img_emb, axis=1, keepdims=True)
#     return img_emb, img_names


def load_clip_model(model_name=None):
    if model_name is None:
        model = SentenceTransformer("clip-ViT-B-32")
    else:
        NotImplementedError
    return model
