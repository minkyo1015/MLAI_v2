# src/agents/researcher.py
from langchain_core.messages import HumanMessage
from src.tools.web_search import tavily_web_search

def research_node(state):
    """
    'topic'을 받아 웹 리서치를 수행하고 'research_data'를 업데이트합니다.
    """
    print("--- 1. Researcher 노드 ---")
    topic = state['topic']
    
    # 웹 검색 도구 실행
    search_results = tavily_web_search.invoke(topic)
    
    # 구조화된 로그(dict) 및 메시지 추가 [cite: 141]
    log_message = f"주제 '{topic}'에 대한 리서치 완료. (결과 길이: {len(search_results)})"
    print(log_message)
    
    return {
        "research_data": search_results,
        "messages": [HumanMessage(content=log_message)]
    }