"""
LLM Factory for flexible model selection.
Supports OpenAI and Google Gemini based on available API keys.
"""
import os
from typing import Union

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

from utils.config import MODEL_NAME, GEMINI_MODEL, LLM_PROVIDER
print(f"DEBUG: Using GEMINI_MODEL = {GEMINI_MODEL}")


def get_llm(temperature: float = 0.7) -> Union[ChatOpenAI, ChatGoogleGenerativeAI]:
    """
    Get LLM instance based on available API keys.
    Priority: Gemini (if GOOGLE_API_KEY exists) > OpenAI (if OPENAI_API_KEY exists)
    
    Args:
        temperature: Temperature for the LLM
        
    Returns:
        LLM instance (ChatOpenAI or ChatGoogleGenerativeAI)
        
    Raises:
        ValueError: If neither API key is available
    """
    provider = LLM_PROVIDER
    google_api_key = os.getenv("GOOGLE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    def build_gemini():
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not set but Gemini provider requested.")
        if not ChatGoogleGenerativeAI:
            raise ValueError("langchain-google-genai is not installed.")
        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            temperature=temperature,
            google_api_key=google_api_key,
            convert_system_message_to_human=True  # Gemini quirk: converts system messages to human
        )
    
    def build_openai():
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not set but OpenAI provider requested.")
        if not ChatOpenAI:
            raise ValueError("langchain-openai is not installed.")
        return ChatOpenAI(
            model=MODEL_NAME,
            temperature=temperature,
            openai_api_key=openai_api_key
        )
    
    # Explicit provider selection
    if provider == "gemini":
        return build_gemini()
    if provider == "openai":
        return build_openai()
    
    # Auto mode: prefer OpenAI per assignment requirement, fall back to Gemini.
    if openai_api_key and ChatOpenAI:
        return build_openai()
    if google_api_key and ChatGoogleGenerativeAI:
        return build_gemini()
    
    raise ValueError(
        "No API key found. Please set OPENAI_API_KEY or GOOGLE_API_KEY (and optionally STORY_LLM_PROVIDER)."
    )
