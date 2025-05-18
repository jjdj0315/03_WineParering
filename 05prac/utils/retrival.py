import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

index_name = "winepairing"
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY")
)

vectorstore = PineconeVectorStore(
    embedding=embedding,
    index_name=index_name,
    pinecone_api_key=os.getenv("PINECONE_API_KEY"),
)


def wine_search(query):
    return vectorstore.similarity_search(query)
