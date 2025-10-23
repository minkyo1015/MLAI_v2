# tests/test_tools.py
import pytest
import os
from unittest.mock import patch
from src.tools.web_search import tavily_web_search

# pytest의 mocker fixture를 사용
def test_tavily_search_no_result(mocker):
    """
    검색 결과가 0건일 때의 예외 처리를 테스트합니다. [cite: 81-83]
    """
    # TavilySearchResults의 .invoke 메서드를 mock합니다. (결과가 비어있도록)
    mocker.patch(
        "src.tools.web_search.TavilySearchResults.invoke", 
        return_value=[]
    )
    
    query = "존재하지않는쿼리zzz"
    result = tavily_web_search.invoke(query)
    
    assert "결과가 없습니다" in result

@patch.dict(os.environ, {"TAVILY_API_KEY": "fake_key"})
def test_tavily_search_success(mocker):
    """
    검색이 성공했을 때의 포맷을 테스트합니다.
    """
    mock_results = [
        {"url": "http://example.com", "content": "이것은 테스트 콘텐츠입니다."}
    ]
    mocker.patch(
        "src.tools.web_search.TavilySearchResults.invoke",
        return_value=mock_results
    )
    
    result = tavily_web_search.invoke("테스트")
    
    assert "http://example.com" in result
    assert "테스트 콘텐츠입니다" in result