# tests/test_end_to_end.py
import pytest
from unittest.mock import patch
from src.workflows.graph import create_graph

@pytest.fixture
def app():
    """
    테스트용으로 컴파일된 app을 반환하는 fixture
    """
    # 실제 API 호출을 방지하기 위해 도구들을 Mocking
    with patch('src.agents.researcher.tavily_web_search.invoke', return_value="Mocked research data"), \
         patch('src.agents.writer.summarize_text.invoke', return_value="Mocked summary"), \
         patch('langchain_openai.ChatOpenAI.invoke') as mock_llm_invoke:
        
        # LLM 호출 순서에 따라 다른 Mock 반환 값 설정
        mock_llm_invoke.side_effect = [
            type('obj', (object,), {'content': 'Mocked Draft Blog Post'}), # 1. Writer
            type('obj', (object,), {'content': '{"feedback": [{"severity": "경미", "comment": "Mocked minor feedback"}]}'}), # 2. Critic (JSON 파싱을 위해 .content 사용)
            type('obj', (object,), {'content': 'Mocked Final Blog Post based on feedback'}) # 3. Editor
        ]
        
        app = create_graph()
        yield app

def test_end_to_end_flow(app):
    """
    그래프의 End-to-End 통합 테스트
    """
    inputs = {
        "topic": "Test Topic",
        "max_iterations": 3,
        "iteration": 0,
        "messages": []
    }
    
    # app.invoke 실행
    result = app.invoke(inputs)
    
    # 최종 결과물이 문자열(str) 형태로 'final_post'에 담겼는지 확인 [cite: 92]
    assert isinstance(result.get("final_post"), str)
    assert "Mocked Final Blog Post" in result.get("final_post")
    
    # Critic의 피드백이 경미했으므로 iteration은 1회로 끝나야 함
    assert result.get("iteration") == 1