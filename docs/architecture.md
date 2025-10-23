# 아키텍처 상세 (architecture.md)

## 1. 컴포넌트 다이어그램



## 2. State 스키마 (`src/utils/state.py`)

[cite_start]`ProjectState`는 `TypedDict`로 정의되며, 그래프의 모든 상태를 관리합니다[cite: 109].

* `topic: str`: 사용자가 입력한 초기 주제
* `iteration: int`: 현재 반복 횟수 (무한 루프 방지용)
* `max_iterations: int`: 최대 허용 반복 횟수
* `research_data: str`: `research_node`가 수집한 원본 데이터
* `draft: str`: `write_node`가 작성한 초안
* `feedback: List[str]`: `critique_node`가 생성한 JSON 문자열 피드백 리스트
* `final_post: str`: `edit_node`가 작성한 최종 결과물
* [cite_start]`messages: Annotated[list, operator.add]`: 모든 노드의 로그 메시지를 누적 저장 [cite: 38]

## [cite_start]3. 에러/재시도/폴백 정책 [cite: 110]

1.  **도구 레벨 (Tool-Level):**
    * **대상:** `tavily_web_search`
    * [cite_start]**정책:** `tenacity` 라이브러리를 사용한 지수 백오프(Exponential Backoff)[cite: 67].
    * [cite_start]**설정:** 0.5초 대기($2^0 * 0.5$)로 시작, 최대 3회 시도[cite: 67].
    * [cite_start]**폴백:** 3회 재시도 실패 시, 사용자 친화적 에러 메시지를 `research_data`에 반환합니다[cite: 68, 144].

2.  **흐름 레벨 (Flow-Level):**
    * **대상:** `critique` $\rightarrow$ `write` 재작성 루프
    * [cite_start]**정책:** `should_revise` 함수가 `state['iteration']`과 `state['max_iterations']`를 비교[cite: 69].
    * [cite_start]**폴백:** 심각한 피드백을 받았더라도 `iteration`이 `max_iterations`에 도달하면, 재작성을 중단하고 강제로 `edit` 노드로 이동하여 작업을 종료시킵니다 (무한 루프 방지).