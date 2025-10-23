# src/utils/state.py
from typing import TypedDict, Annotated, List
import operator

class ProjectState(TypedDict):
    """
    LangGraph의 전체 상태를 정의하는 TypedDict입니다.
    """
    
    # 입력
    topic: str
    
    # 재시도/반복 제어
    iteration: int
    max_iterations: int
    
    # 에이전트별 산출물
    research_data: str
    draft: str
    feedback: List[str] # Critic은 여러 피드백을 줄 수 있으므로 List
    final_post: str
    
    # 모든 노드의 메시지를 누적
    messages: Annotated[list, operator.add]