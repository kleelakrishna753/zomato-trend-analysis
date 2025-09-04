import openai
import numpy as np
from config import EMBED_MODEL, SIMILARITY_THRESHOLD

def cosine_sim(vec1, vec2):
    v1, v2 = np.array(vec1), np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def cluster_topics(unique_topics):
    # Get embeddings
    emb_response = openai.Embedding.create(
        model=EMBED_MODEL,
        input=list(unique_topics)
    )
    embeddings = {item['index']: item['embedding'] for item in emb_response['data']}
    topic_list = list(unique_topics)

    cluster_map = {}
    clusters = []

    for idx, topic in enumerate(topic_list):
        vec = embeddings[idx]
        found_cluster = False
        for rep_idx in clusters:
            sim = cosine_sim(vec, embeddings[rep_idx])
            if sim > SIMILARITY_THRESHOLD:
                cluster_map[topic] = topic_list[rep_idx]
                found_cluster = True
                break
        if not found_cluster:
            clusters.append(idx)
            cluster_map[topic] = topic

    return cluster_map
