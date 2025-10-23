# API 및 실행 파이프라인 (api.md)

본 프로젝트는 REST API가 아닌 `examples/run_example.py`를 통해 실행되는 파이프라인입니다.

## 실행 파이프라인 (Graph Execution)

`app.invoke(inputs)` 호출 시 실행되는 시퀀스입니다.

1.  **Input (입력):**
    * `ProjectState`의 초기값 (최소 `topic`, `max_iterations`, `iteration`, `messages` 필요)

2.  **Flow (흐름):**
    1.  `research_node`: `topic` $\rightarrow$ `research_data`
    2.  `write_node`: `research_data` $\rightarrow$ `draft`, `iteration` + 1
    3.  `critique_node`: `draft` $\rightarrow$ `feedback`
    4.  `should_revise` (Conditional Edge):
        * IF (`feedback` 심각 AND `iteration` < `max_iterations`) $\rightarrow$ GOTO 2. `write_node`
        * ELSE $\rightarrow$ GOTO 5. `edit_node`
    5.  `edit_node`: `draft` + `feedback` $\rightarrow$ `final_post`
    6.  `END`

3.  **Output (출력):**
    * 모든 필드가 채워진 최종 `ProjectState` (Dict)
    * `final_state['final_post']` (최종 블로그 포스트)