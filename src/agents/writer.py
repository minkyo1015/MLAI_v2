# src/agents/writer.py
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm import get_llm
from src.tools.summarizer import summarize_text

def write_node(state):
    """
    'research_data'를 요약/활용하여 블로그 초안('draft')을 작성합니다.
    'iteration' 횟수를 1 증가시킵니다.
    """
    print(f"--- 2. Writer 노드 (반복 {state.get('iteration', 0) + 1}) ---")
    topic = state['topic']
    research_data = state['research_data']
    
    # 도구(요약기)를 사용해 리서치 데이터 압축
    summary = summarize_text.invoke(research_data)
    
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "당신은 IT 전문 블로거입니다. "
         "제공된 요약 자료를 바탕으로 800~1200자 분량의 전문적인 블로그 포스트를 작성해 주세요. " # [cite: 21]
         "제목, 서론, 본론, 결론의 구조를 갖춰주세요."),
        ("user", "주제: {topic}\n\n요약 자료:\n{summary}")
    ])
    
    chain = prompt | llm
    draft = chain.invoke({"topic": topic, "summary": summary}).content
    
    log_message = "블로그 초안 작성 완료."
    print(log_message)
    
    # iteration + 1 (루프 제어용)
    new_iteration = state.get('iteration', 0) + 1
    
    return {
        "draft": draft,
        "iteration": new_iteration,
        "messages": [HumanMessage(content=log_message)]
    }