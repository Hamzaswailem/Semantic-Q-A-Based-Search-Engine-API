from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline
import uuid
import os




#keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
model_name = os.getenv("model_name")
google_model = os.getenv("google_model")

class QdrantService:
    #Initialization
    def __init__(self,collection_name: str):
        self.collection_name = collection_name
        self.client = QdrantClient(host="localhost", port=6333)
        self.embedding_model = HuggingFaceEmbeddings(model_name=model_name)
        self._create_collection()



    #Create Collection
    def _create_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384,  distance=Distance.COSINE)
            )


    def add_texts (self, texts: list[str], embeddings: list[list[float]]):
        embeddings = self.embedding_model.embed_documents(texts)

        points = []
        for text, vector in zip(texts, embeddings):
            points.append({
                "id": str(uuid.uuid4()),     
                "vector": vector,
                "payload": {"text": text}
            })
            
                
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
                )

    def search(self, query: str, top_k: int = 1):
        query_embedding = self.embedding_model.embed_query(query)
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        return [hit.payload for hit in hits]



    def answer_with_local_llm(self, query: str, top_k: int = 5) -> str:
            #  Get relevant context
            matches = self.search(query=query, top_k=top_k)
            context = "\n\n".join([m['text'] for m in matches if 'text' in m])

            if not context:
                return "No relevant context found."

            # Load local Hugging Face model 
            qa_pipeline = pipeline(
                "text2text-generation",
                model=google_model, 
                tokenizer="google/flan-t5-base"
            )

            #Construct prompt
            prompt = f"""You are a helpful AI assistant. Based on the context below, answer the question as best as you can.
                    Context:
                    {context}
                    Question: {query}
                    Answer:"""

            # Get response
            try:
                result = qa_pipeline(prompt, max_new_tokens=200, do_sample=False)
                return result[0]['generated_text']
            except Exception as e:
                return f"Error during generation: {str(e)}"


