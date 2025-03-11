from sentence_transformers import SentenceTransformer, util
import torch
import pickle
import os

class KB_Search:
    def __init__(self, file_path, model_name="all-MiniLM-L6-v2"):
        self.file_path = file_path
        self.embed_path = "assets/KB_embeddings.pkl"
        self.model_name = model_name
        self.model = None
        self.chunks = None
        self.embeded_chunks = None

    def load_kb(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = text.strip().split("\n\n")
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def embed_chunks(self):
        if not self.model:
            self.model = SentenceTransformer(self.model_name)

        self.chunks = self.load_kb()
        self.embeded_chunks = self.model.encode(self.chunks, convert_to_tensor=True)

        with open(self.embed_path, "wb") as f:
            pickle.dump((self.chunks, self.embeded_chunks), f)

        return self.chunks, self.embeded_chunks

    def find_knowledge(self, query, top_n=10):
        if os.path.exists(self.embed_path):
            with open(self.embed_path, "rb") as f:
                self.chunks, self.embeded_chunks = pickle.load(f)

        if self.chunks is None or self.embeded_chunks is None:
            self.embed_chunks()

        if not self.model:
            self.model = SentenceTransformer(self.model_name)

        embeded_query = self.model.encode(query, convert_to_tensor=True)
        sim_scores = util.cos_sim(embeded_query, self.embeded_chunks)[0]
        top_chunks = sim_scores.argsort(descending=True)[:top_n]
        relevant_chunks = [self.chunks[i] for i in top_chunks]

        # for rc in relevant_chunks:
        #     print(rc)

        return relevant_chunks


# kb = KB_Search("assets/kb.txt")

# while True:
#     q = input("Enter: ")
#     kb.find_knowledge(q)
