# tests/test_graph_flow.py
import pytest
from src.utils.state import ProjectState
from src.workflows.graph import should_revise

# 과제 필수 요건: 조건부 라우팅 케이스 [cite: 142]

def test_should_revise_triggers_rewrite():
    """
    '심각' 피드백이 있고, 반복 횟수가 최대치 미만일 때 'write'를 반환하는지 테스트
    """
    state = ProjectState(
        topic="test", research_data="", draft="", final_post="", messages=[],
        feedback=['{"severity": "심각", "comment": "내용 전면 수정 필요"}'],
        iteration=1,
        max_iterations=3
    )
    result = should_revise(state)
    assert result == "write"

def test_should_revise_triggers_edit_minor():
    """
    '경미' 피드백이 있을 때 'edit'를 반환하는지 테스트
    """
    state = ProjectState(
        topic="test", research_data="", draft="", final_post="", messages=[],
        feedback=['{"severity": "경미", "comment": "오타 수정"}'],
        iteration=1,
        max_iterations=3
    )
    result = should_revise(state)
    assert result == "edit"

def test_should_revise_triggers_edit_max_iterations():
    """
    '심각' 피드백이 있더라도, 최대 반복 횟수에 도달하면 'edit'를 반환하는지 테스트 (무한 루프 방지) 
    """
    state = ProjectState(
        topic="test", research_data="", draft="", final_post="", messages=[],
        feedback=['{"severity": "심각", "comment": "내용 전면 수정 필요"}'],
        iteration=3,
        max_iterations=3
    )
    result = should_revise(state)
    assert result == "edit"