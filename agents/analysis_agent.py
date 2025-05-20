from typing import Dict
from langchain_openai import ChatOpenAI
import json

def analyze_trends(state: Dict) -> Dict:
    """analysis 노드 - 요약 데이터를 분석하여 
    해당 트렌드 장점 및 주의점 지표 식별"""
    
    # LLM 초기화
    llm = ChatOpenAI(temperature=0.1, model="gpt-4")
    
    # 상태에서 요약 데이터 가져오기
    summary = state.get("summary", {})
    summary_text = json.dumps(summary)
    
    # 트렌드 평가 지표 프롬프트
    metrics_prompt = f"""
    당신은 AI 기술 트렌드 분석가입니다. 다음 검색 결과 요약을 바탕으로:
    
    {summary_text}
    
    다음 트렌드 평가 기준에 대한 수치 지표를 0-10 척도로 결정해주세요:
    1. 연구 활동: 관련 논문 출판 수 증가 추세
    2. 시장 반응: 투자 규모 및 성장률
    3. 기업 채택: 주요 기업들의 기술 도입 속도
    4. 검색 관심도: 검색 키워드 트렌드
    5. 인재 수요: 관련 직무 채용 증가율
    
    요약에 언급된 주요 AI 트렌드 각각에 대해 이 지표들을 제공해주세요.
    트렌드 이름을 키로, 5가지 지표를 값으로 하는 JSON 객체로 응답해주세요.
    """
    
    # 지표 생성
    metrics_response = llm.invoke(metrics_prompt)
    try:
        trend_metrics = json.loads(metrics_response.content)
    except:
        trend_metrics = {"error": "Failed to parse metrics"}
    
    # 상위 트렌드 분석 프롬프트
    top_trends_prompt = f"""
    요약 및 계산한 지표를 바탕으로:
    
    요약: {summary_text}
    지표: {json.dumps(trend_metrics)}
    
    향후 5년간 상위 5개 AI 트렌드를 식별해주세요. 각 트렌드에 대해 다음 정보를 제공하세요:
    1. 트렌드 이름
    2. 간략한 설명
    3. 중요도 점수(1-10)
    4. 잠재적 비즈니스 영향(1-10)
    5. 주류 도입까지의 예상 타임라인
    
    이 다섯 가지 속성을 포함하는 객체 배열로 JSON 형식의 응답을 제공해주세요.
    """
    
    # 상위 트렌드 생성
    top_trends_response = llm.invoke(top_trends_prompt)
    try:
        top_trends = json.loads(top_trends_response.content)
    except:
        top_trends = [{"error": "Failed to parse top trends"}]
    
    # 상세 트렌드 분석 프롬프트
    analysis_prompt = f"""
    요약, 지표 및 식별된 상위 트렌드를 바탕으로:
    
    요약: {summary_text}
    지표: {json.dumps(trend_metrics)}
    상위 트렌드: {json.dumps(top_trends)}
    
    각 상위 트렌드에 대한 상세 분석을 제공해주세요:
    1. 현재 개발 상태
    2. 성장 궤적
    3. 산업 영향(트렌드당 최소 3개 산업)
    4. 기회와 도전과제
    5. 기업을 위한 구현 고려사항
    
    트렌드 이름을 키로, 상세 분석 객체를 값으로 하는 JSON 객체로 응답해주세요.
    """
    
    # 트렌드 분석 생성
    analysis_response = llm.invoke(analysis_prompt)
    try:
        trend_analysis = json.loads(analysis_response.content)
    except:
        trend_analysis = {"error": "Failed to parse trend analysis"}
    
    # 상태 업데이트
    return {
        "trend_metrics": trend_metrics,
        "top_trends": top_trends,
        "trend_analysis": trend_analysis
    }