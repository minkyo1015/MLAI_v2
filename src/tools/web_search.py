# src/tools/web_search.py
# src/tools/web_search.py
import os
# from langchain_community.tools.tavily_search import TavilySearchResults # (기존)
from langchain_tavily import TavilySearch # (수정)
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from langchain_core.tools import tool
# tenacity를 사용한 지수 백오프 설정
# (이하 코드는 동일)
# ... (rest of the file)

# tenacity를 사용한 지수 백오프 설정
# 0.5초부터 시작해 2배씩 증가하며(wait_exponential), 최대 3회 시도(stop_after_attempt)
search_retry_decorator = retry(
    wait=wait_exponential(multiplier=1, min=0.5, max=10),
    stop=stop_after_attempt(3)
)

@tool
@search_retry_decorator
def tavily_web_search(query: str) -> str:
    """
    Tavily API를 사용해 웹 검색을 수행하고 결과를 문자열로 반환합니다.
    네트워크 오류 또는 API 5xx 오류 시 지수 백오프로 3회 재시도합니다.
    
    Args:
        query (str): 검색할 쿼리
        
    Returns:
        str: 검색 결과 요약 문자열
    """
    try:
        # Tavily API 키가 설정되지 않았으면 에러 발생
        if not os.getenv("TAVILY_API_KEY"):
            return "오류: TAVILY_API_KEY가 설정되지 않았습니다. 관리자에게 문의하세요."

        # k=5: 5개의 관련 문서를 찾아 요약합니다.
        tavily = TavilySearch(max_results=5) # (수정)
        results = tavily.invoke(query)
        
        if not results:
            # 과제 요구사항: 빈 결과에 대한 처리 [cite: 68]
            return f"'{query}'에 대한 검색 결과가 없습니다."
        
        # LLM이 재활용하기 쉽도록 구조화된 문자열로 반환 [cite: 64]
        return "\n".join([f"- (Source: {res['url']})\n{res['content']}" for res in results])
    
    except RetryError as e:
        # 과제 요구사항: 재시도 실패 시 사용자 친화적 메시지 반환 [cite: 144]
        return f"네트워크 오류: 검색 도구 호출에 3회 실패했습니다. (오류: {e})"
    except Exception as e:
        return f"검색 중 알 수 없는 오류 발생: {e}"