# src/agents/editor.py
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm import get_llm

def edit_node(state):
    """
    'draft'와 'feedback'을 바탕으로 최종본('final_post')을 작성합니다.
    """
    print("--- 4. Editor 노드 ---")
    draft = state['draft']
    feedback = state['feedback']
    
    # feedback list(json str)를 하나의 문자열로 합침
    feedback_str = "\n- ".join(feedback)
    
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 수석 편집자입니다. "
                 "제공된 초안과 피드백을 바탕으로, 완성도 높은 최종 블로그 포스트를 작성해 주세요."),
        ("user", "초안:\n{draft}\n\n피드백:\n- {feedback}\n\n위 피드백을 반영한 최종본을 작성해 주세요.")
    ])
    
    chain = prompt | llm
    final_post = chain.invoke({"draft": draft, "feedback": feedback_str}).content
    
    log_message = "최종본 작성 완료."
    print(log_message)
    
    return {
        "final_post": final_post,
        "messages": [HumanMessage(content=log_message)]
    }