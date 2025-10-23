# src/agents/critic.py
import json
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.utils.llm import get_llm

def critique_node(state):
    """
    'draft'를 검토하고 'feedback'을 생성합니다.
    피드백은 JSON 형식으로 구조화하여 반환합니다.
    """
    print("--- 3. Critic 노드 ---")
    topic = state['topic']
    draft = state['draft']
    
    llm = get_llm()
    
    # JSON 출력을 위한 파서 설정
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "당신은 까다로운 편집장입니다. 다음 블로그 초안을 검토하고 "
         "수정 제안 사항을 JSON 형식으로 반환해 주세요. "
         "피드백이 2개 이상 필요합니다. "
         "만약 초안이 주제와 관련 없거나 매우 부실하면 'severity' 필드에 '심각' 또는 '전면 수정'을 포함하세요. "  #[cite: 51]
         "그렇지 않으면 '경미' 또는 '일부 수정'으로 설정하세요.\n"
         "{format_instructions}"),
        ("user", "주제: {topic}\n\n초안:\n{draft}")
    ]).partial(format_instructions=parser.get_format_instructions())
    
    chain = prompt | llm | parser
    
    try:
        feedback_json = chain.invoke({"topic": topic, "draft": draft})
        # LLM이 재활용하기 쉬운 dict(str) 형태로 저장
        feedback_list = [json.dumps(fb, ensure_ascii=False) for fb in feedback_json.get("feedback", [])]
        
        log_message = f"피드백 생성 완료 (총 {len(feedback_list)}개)"
        print(log_message)
        
        return {
            "feedback": feedback_list,
            "messages": [HumanMessage(content=log_message)]
        }
    except Exception as e:
        log_message = f"Critic 오류: 피드백 JSON 파싱 실패 ({e})"
        print(log_message)
        return {
            # 오류 발생 시, 루프를 방지하기 위해 강제로 경미한 피드백을 주어 edit 노드로 넘김
            "feedback": [json.dumps({"severity": "경미", "comment": "피드백 생성 중 오류 발생"}, ensure_ascii=False)],
            "messages": [HumanMessage(content=log_message)]
        }