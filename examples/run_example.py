# examples/run_example.py
import autorootcwd
import os
from dotenv import load_dotenv
from src.workflows.graph import create_graph

# .env 파일 로드 (API 키)
load_dotenv()

# API 키 설정 확인
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("TAVILY_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY 또는 TAVILY_API_KEY가 .env 파일에 설정되지 않았습니다.")

def run_project():
    """
    리서치 에이전트 그래프를 실행합니다.
    """
    
    # 1. 그래프 컴파일
    app = create_graph()
    
    # 2. 입력값 정의
    # (주의: 실제 실행 시 topic을 원하는 주제로 변경하세요)
    topic_to_research = "멀티모달 딥페이크 탐지 기술의 최신 동향"
    
    inputs = {
        "topic": topic_to_research,
        "max_iterations": 3,
        "iteration": 0,
        "messages": [] # 메시지 초기화
    }
    
    print(f"--- 🚀 리서치 에이전트 시작 (주제: {topic_to_research}) ---")
    
    # 3. 그래프 실행
    # .stream() 대신 .invoke()를 사용해 최종 결과만 확인
    final_state = app.invoke(inputs)
    
    # 4. 최종 결과 출력
    print("\n--- ✅ 작업 완료 ---")
    print("\n[최종 블로그 포스트]:")
    print(final_state.get("final_post", "최종본이 생성되지 않았습니다."))
    
    # print("\n[전체 상태 로그]:")
    # print(final_state)

if __name__ == "__main__":
    run_project()