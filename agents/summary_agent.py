from typing import Dict
from langchain_openai import ChatOpenAI
import json

def summarize_search_results(state: Dict) -> Dict:
    """Search Summarization 노드 - 검색 결과 요약"""
    
    # LLM 초기화
    llm = ChatOpenAI(temperature=0.1)
    
    # 검색 결과 텍스트 결합
    combined_results = ""
    for item in state.get("search_results", []):
        combined_results += f"검색어: {item['query']}\n"
        combined_results += f"결과: {item['result']}\n\n"
    
    # 요약 프롬프트 생성
    summary_prompt = f"""
    당신은 기술 트렌드 분석 전문가입니다. 다음의 AI 기술 트렌드에 관한 검색 결과를 검토하고 
    주요 영역별로 포괄적인 요약을 제공해주세요.
    
    검색 결과:
    {combined_results}
    
    다음 항목을 포함하여 검색 결과를 잘 구조화된 요약으로 제공해주세요:
    1. 주요 AI 기술 트렌드
    2. 이러한 기술들의 시간적 전망
    3. 주요 산업 응용 분야
    4. 투자 패턴
    5. 도입 관련 과제와 기회
    
    응답을 이 카테고리를 키로 하는 JSON 형식으로 구성해주세요.
    """
    
    # 요약 생성
    summary_response = llm.invoke(summary_prompt)
    summary = summary_response.content
    
    # JSON 형식으로 파싱
    try:
        summary_dict = json.loads(summary)
    except:
        summary_dict = {"raw_summary": summary}
    
    # 상태 업데이트
    return {"summary": summary_dict}