# src/tools/summarizer.py
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm import get_llm

@tool
def summarize_text(text: str) -> str:
    """
    입력된 긴 텍스트를 핵심만 요약합니다.
    Writer 에이전트가 리서치 자료를 압축할 때 사용합니다.
    
    Args:
        text (str): 요약할 원본 텍스트
        
    Returns:
        str: 요약된 텍스트
    """
    if not text:
        return "요약할 텍스트가 없습니다."
        
    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 전문 요약기입니다. 입력된 텍스트의 핵심 내용을 블로그 포스트에 쓰기 좋도록 압축해 주세요."),
            ("user", "{text_to_summarize}")
        ])
        
        chain = prompt | llm
        summary = chain.invoke({"text_to_summarize": text})
        return summary.content
    except Exception as e:
        # LLM 호출 실패 시
        return f"요약 중 오류 발생: {e}"