# 프로젝트: LangGraph 기반 리서치 에이전트

[cite_start]**선택 트랙: A. 리서치 작성 Multi-Agent** [cite: 32]

## 1. 프로젝트 개요

본 프로젝트는 LangGraph를 사용하여 특정 주제에 대한 리서치, 초안 작성, 피드백, 수정을 자동화하는 멀티 에이전트 시스템입니다. 'Researcher', 'Writer', 'Critic', 'Editor'의 4개 에이전트가 협력하여 최종 블로그 포스트를 생성합니다.

## 2. 아키텍처



* **State:** `ProjectState` (TypedDict)
* **Nodes (Agents):**
    1.  `research`: 주제에 대해 Tavily 웹 검색 수행
    2.  `write`: 검색 결과를 요약/바탕으로 초안 작성 (Iteration + 1)
    3.  `critique`: 초안 검토 및 JSON 형식의 피드백(심각도 포함) 생성
    4.  `edit`: 피드백을 반영하여 최종본 작성
* **Tools:**
    1.  [cite_start]`tavily_web_search`: 에러 처리 및 지수 백오프 재시도 포함 
    2.  `summarize_text`: LLM을 이용한 텍스트 요약
* **Conditional Edge (핵심):**
    * [cite_start]`critique` 노드 이후, `should_revise` 함수가 피드백의 '심각도'와 'iteration' 횟수를 검사합니다[cite: 50].
    * (심각 && 반복 < 최대) [cite_start]$\rightarrow$ `write` (재작성) [cite: 52-53]
    * (경미 || 반복 >= 최대) [cite_start]$\rightarrow$ `edit` (수정) [cite: 54]

## 3. 설치 및 실행

### 3.1 설치

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate

# 2. 필요 라이브러리 설치
pip install -r requirements.txt