from typing import List
from fastapi import File, Form, APIRouter, FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
from qdrant_client.models import VectorParams, Distance 
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.services.pdf_parser import Parser
from app.services.embedding import Embedder
from app.services.qdrant_manger import QdrantService



#keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
model_name = os.getenv("model_name")
openai_model = os.getenv("openai_model")



#uvicorn app.api.documents:app --reload  #to run the code#


router = APIRouter()





@router.post("/upload")
async def upload_document(files: List[UploadFile] = File(...)):
    results = []

    qdrant_service = QdrantService(collection_name="pdf_chunks")

    # Clear existing collection  
    qdrant_service.client.recreate_collection(
        collection_name="pdf_chunks",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    qdrant_service = QdrantService(collection_name="pdf_chunks")

    for file in files:
        try:
            # Read 
            file_bytes = await file.read()
            file_stream = BytesIO(file_bytes)

            # Extract text
            text = Parser.extract_text(file_stream).strip() 
            if isinstance(text, list):
                text = "\n".join(text) 
            if not text.strip():
                    raise ValueError(f"No text extracted from {file.filename}")


            #chunk text
            chunks = Parser.chunk_text(text)
            if not chunks:
                    raise ValueError("No chunks created - check chunking parameters")

            #Embeding & storing vectors
            embeddings = Embedder.embed(chunks)
            qdrant_service.add_texts(chunks, embeddings)
            results.append({"filename": file.filename, "chunks_added": len(chunks)}) 
            

        #Error handeling
        except Exception as e:
            print(f"Error processing {file.filename}: {str(e)}")
            continue
        except ValueError as e:
            print(f"Validation error processing {file.filename}: {str(e)}")
            continue

    return JSONResponse(content={
        "message": "Document(s) processed successfully",
        "results":results}
        )



@router.post("/query")
async def query_document(
    Questions: str = Form(..., min_length=3, max_length=1000, description="Your search question"),
    top_k: int = Form(5, ge=1, le=20, description="Number of results to return")) -> JSONResponse:

        qdrant_service = QdrantService(collection_name="pdf_chunks")

        answer = qdrant_service.answer_with_local_llm(query=Questions, top_k=top_k)
        
        return JSONResponse(content={
        "message": "Query executed successfully",
        "answer": answer
        })
    
from fastapi import FastAPI
app = FastAPI()

try:
    app.include_router(router, prefix="/api")
except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))



