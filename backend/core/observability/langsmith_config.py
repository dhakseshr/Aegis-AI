"""LangSmith observability setup."""
import os
from langsmith import Client
from langchain.callbacks import LangChainTracer

def configure_langsmith():
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "aegis-ai")
    return Client()

def get_tracer(run_name: str) -> LangChainTracer:
    return LangChainTracer(project_name=os.getenv("LANGCHAIN_PROJECT", "aegis-ai"))
