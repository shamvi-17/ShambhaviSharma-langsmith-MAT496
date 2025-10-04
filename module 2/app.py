import os
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langsmith import traceable
from anthropic import Anthropic
from typing import List
import nest_asyncio

MODEL_NAME = "claude-sonnet-4-5-20250929"
MODEL_PROVIDER = "anthropic"
APP_VERSION = 1.0
RAG_SYSTEM_PROMPT = """You are an assistant for question-answering tasks.

Use the following pieces of retrieved context to answer the latest question in the conversation.

If you don't know the answer, just say that you don't know.

Use three sentences maximum and keep the answer concise.
"""

anthropic_client = Anthropic()


def get_vector_db_retriever():
    persist_path = os.path.join(tempfile.gettempdir(), "union.parquet")

    # Use HuggingFace embeddings - this is a popular, free, open-source model
    embd = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # Change to 'cuda' if you have GPU
        encode_kwargs={'normalize_embeddings': True}
    )

    # If vector store exists, then load it
    if os.path.exists(persist_path):
        vectorstore = SKLearnVectorStore(
            embedding=embd,
            persist_path=persist_path,
            serializer="parquet"
        )
        return vectorstore.as_retriever(lambda_mult=0)

    # Otherwise, index LangSmith documents and create new vector store
    ls_docs_sitemap_loader = SitemapLoader(
        web_path="https://docs.smith.langchain.com/sitemap.xml",
        continue_on_failure=True
    )
    ls_docs = ls_docs_sitemap_loader.load()

    # Use character-based splitter instead of tiktoken (OpenAI-specific)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    doc_splits = text_splitter.split_documents(ls_docs)

    vectorstore = SKLearnVectorStore.from_documents(
        documents=doc_splits,
        embedding=embd,
        persist_path=persist_path,
        serializer="parquet"
    )
    vectorstore.persist()
    return vectorstore.as_retriever(lambda_mult=0)


nest_asyncio.apply()
retriever = get_vector_db_retriever()

"""
retrieve_documents - Returns documents fetched from a vectorstore based on the user's question
"""


@traceable(run_type="chain")
def retrieve_documents(question: str):
    return retriever.invoke(question)


"""
generate_response - Calls `call_anthropic` to generate a model response after formatting inputs
"""


@traceable(run_type="chain")
def generate_response(question: str, documents):
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)
    user_message = f"Context: {formatted_docs} \n\n Question: {question}"
    return call_anthropic(user_message)


"""
call_anthropic - Returns the chat completion output from Anthropic
"""


@traceable(
    run_type="llm",
    metadata={
        "ls_provider": MODEL_PROVIDER,
        "ls_model_name": MODEL_NAME
    }
)
def call_anthropic(user_message: str) -> str:
    response = anthropic_client.messages.create(
        model=MODEL_NAME,
        max_tokens=1024,
        system=RAG_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return response


"""
langsmith_rag - Calls `retrieve_documents` to fetch documents
- Calls `generate_response` to generate a response based on the fetched documents
- Returns the model response
"""


@traceable(run_type="chain")
def langsmith_rag(question: str):
    documents = retrieve_documents(question)
    response = generate_response(question, documents)
    return response.content[0].text