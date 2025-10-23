# src/utils/llm.py

from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_llm():
    """
    Gemini LLM (gemini-1.0-pro)을 로드합니다.
    """
    # 'gemini-pro' 대신 'gemini-1.0-pro' 모델을 사용합니다.
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", temperature=0)
    return llm