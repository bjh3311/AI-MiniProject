from typing import Dict
from langchain_openai import ChatOpenAI

def generate_report(state: Dict) -> Dict:
    """Report 노드에서 AI 미래 기술 트렌드 분석 보고서를 생성하는 함수"""
    
    # LLM 초기화
    llm = ChatOpenAI(temperature=0.7, model="gpt-4")
    
    # 상태에서 데이터 가져오기
    summary = state.get("summary", {})
    trend_metrics = state.get("trend_metrics", {})
    top_trends = state.get("top_trends", [])
    trend_analysis = state.get("trend_analysis", {})
    
    # 프롬프트 구성
    report_prompt = f"""
    # AI 미래 기술 트렌드 분석 보고서
    
    ## 개요
    당신은 기술 트렌드 분석 전문가입니다. AI를 포함한 미래 기술을 분석하고, 향후 5년 이내 기업에서 관심있게 봐야할 AI 트렌드 예측 보고서를 작성해 주세요.
    
    ## 분석 기반 데이터
    - 검색 결과 요약: {summary}
    - 트렌드 지표: {trend_metrics}
    - 상위 트렌드: {top_trends}
    - 트렌드 분석: {trend_analysis}
    
    ## 트렌드 평가 논리
    다음 기준을 활용하여 향후 5년 AI 트렌드를 평가해 주세요:
    
    1. **연구 활동**: 관련 논문 출판 수 증가 추세
    2. **시장 반응**: 투자 규모 및 성장률
    3. **기업 채택**: 주요 기업들의 기술 도입 속도
    4. **검색 관심도**: 검색 키워드 트렌드
    5. **인재 수요**: 관련 직무 채용 증가율
    
    ## 보고서 구성 요구사항
    1. **주요 AI 트렌드 요약 (Executive Summary)**
       - 상위 5개 AI 트렌드와 각 트렌드별 중요도
       
    2. **트렌드별 심층 분석 (각 트렌드당)**
       - 현재 기술 발전 상황
       - 발전 속도 및 향후 전망
       - 산업별 영향 (3-5개 주요 산업)
       - 기회 및 도전 과제
       
    3. **기업 적용 전략**
       - 기업 규모별 접근 전략 (대기업 vs. 중소기업)
       - 단계별 도입 로드맵 제안
       - 투자 우선순위 제안
       
    4. **결론 및 제언**
       - 종합적 관점에서의 AI 트렌드 전망
       - 기업이 취해야 할 핵심 액션 아이템
    
    ## 형식 가이드라인
    - 객관적이고 데이터에 근거한 내용
    - 전문적이면서도 이해하기 쉬운 언어
    - 각 섹션마다 명확한 소제목
    - 분석 결과를 뒷받침하는 근거 포함
    - 전체 보고서 분량: 약 2,000단어
    
    이 보고서는 기술 의사결정자들이 향후 AI 투자 및 전략 방향을 설정하는 데 도움이 되는 실용적 가이드가 되어야 합니다.
    """
    
    # 보고서 생성
    report_response = llm.invoke(report_prompt)
    report = report_response.content
    
    # 상태 업데이트
    return {"report": report}