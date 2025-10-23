# src/workflows/graph.py
from langgraph.graph import StateGraph, END
from src.utils.state import ProjectState
from src.agents.researcher import research_node
from src.agents.writer import write_node
from src.agents.critic import critique_node
from src.agents.editor import edit_node

# --- 3.1 조건부 엣지 함수 ---
def should_revise(state: ProjectState):
    """
    Critic의 피드백을 기반으로 재작성(write)할지, 
    수정(edit)할지, 아니면 루프를 종료할지 결정합니다.
    """
    print("--- ? 조건부 엣지 (should_revise) ---")
    feedback = state.get("feedback", [])
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 3)
    
    # 피드백 내용에서 '심각' 또는 '전면' 키워드 확인 
    severe_feedback = any("심각" in f or "전면" in f for f in feedback)
    
    if severe_feedback and iteration < max_iterations:
        # 1. 심각한 피드백이 있고, 최대 반복 횟수 미만 -> 재작성 [cite: 52-53]
        print(f"-> 결정: 재작성 (반복 {iteration}/{max_iterations})")
        return "write"
    else:
        # 2. 피드백이 경미하거나, 최대 반복 횟수 도달 -> 수정 및 종료 [cite: 54]
        if severe_feedback:
            print(f"-> 결정: 최대 반복 도달. 수정으로 강제 이동. (반복 {iteration}/{max_iterations})")
        else:
            print("-> 결정: 피드백 경미. 수정으로 이동.")
        return "edit"

# --- 3.2 그래프 생성 및 컴파일 ---
def create_graph():
    """
    StateGraph를 생성하고 노드와 엣지를 정의합니다.
    """
    
    # StateGraph에 State 클래스 연결
    workflow = StateGraph(ProjectState)

    # 1. 노드 추가
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    workflow.add_node("critique", critique_node)
    workflow.add_node("edit", edit_node)

    # 2. 엣지 연결
    
    # 시작점
    workflow.set_entry_point("research")
    
    # 단순 엣지
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "critique")
    
    # 조건부 엣지 (과제 핵심)
    workflow.add_conditional_edges(
        "critique",       # 시작 노드
        should_revise,    # 조건 함수
        {
            "write": "write", # "write" 반환 시 write 노드로
            "edit": "edit"    # "edit" 반환 시 edit 노드로
        }
    )
    
    # 종료
    workflow.add_edge("edit", END)

    # 3. 그래프 컴파일
    app = workflow.compile()
    
    return app