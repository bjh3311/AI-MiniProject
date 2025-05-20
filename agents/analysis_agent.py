from typing import Dict, List
from langchain_openai import ChatOpenAI
import json
from dotenv import load_dotenv

load_dotenv()

def analyze_trends(state: Dict) -> Dict:
    """
    Analysis 노드 - 요약 데이터를 분석하여 각 키워드에 대한 점수 및 이유 제공
    """
    # 상태에서 요약 데이터 가져오기
    summaries = state.get("summary", [])
    if not summaries:
        state["top_trends"] = []
        return state
    
    # LLM 초기화
    llm = ChatOpenAI(temperature=0.1, model="gpt-4")
    
    top_trends = []
    
    # 각 키워드별로 점수 매기기
    for summary_item in summaries:
        keyword = summary_item.get("keyword", "")
        summary_text = summary_item.get("summary", "")
        
        if not keyword or not summary_text:
            continue
        
        # 트렌드 평가 프롬프트
        scoring_prompt = f"""
        당신은 기술 트렌드 분석 전문가입니다. 다음 키워드 '{keyword}'와 관련된 뉴스 요약을 분석하고, 0-10 점 척도로 점수를 매겨주세요.

        뉴스 요약:
        {summary_text}

        다음 5가지 항목에 대해 각각 0-10점으로 평가한 후, 최종 종합 점수를 계산해주세요:

        1. 시장 성장성: 해당 기술의 시장 규모 및 성장 잠재력
        2. 기업 채택률: 주요 기업들이 해당 기술을 도입하는 속도와 범위
        3. 기술 성숙도: 기술이 얼마나 실용적이고 안정적인지 여부
        4. 혁신 잠재력: 산업과 사회에 가져올 혁신적 변화 가능성
        5. 지속가능성: 단기적 유행이 아닌 장기적 트렌드로 발전할 가능성

        JSON 형식으로 다음 내용을 포함하여 응답해주세요:
        1. 각 항목별 점수(0-10)
        2. 종합 점수(0-10, 소수점 한 자리까지)
        3. 점수에 대한 간결한 근거 설명(100단어 이내)

        응답은 다음 형식의 JSON으로 제공해주세요:
        {{
            "market_growth": 점수,
            "enterprise_adoption": 점수,
            "tech_maturity": 점수,
            "innovation_potential": 점수,
            "sustainability": 점수,
            "overall_score": 종합점수,
            "reason": "점수에 대한 근거 설명"
        }}
        """
        
        # LLM을 사용하여 점수 및 이유 생성
        scoring_response = llm.invoke(scoring_prompt)
        
        try:
            score_data = json.loads(scoring_response.content)
            
            # top_trends에 추가할 형식으로 변환
            trend_item = {
                "keyword": keyword,
                "score": score_data.get("overall_score", 0),
                "reason": score_data.get("reason", "No reason provided")
            }
            
            # 세부 점수도 포함
            trend_item["details"] = {
                "market_growth": score_data.get("market_growth", 0),
                "enterprise_adoption": score_data.get("enterprise_adoption", 0),
                "tech_maturity": score_data.get("tech_maturity", 0),
                "innovation_potential": score_data.get("innovation_potential", 0),
                "sustainability": score_data.get("sustainability", 0)
            }
            
            top_trends.append(trend_item)
            
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 기본값 사용
            top_trends.append({
                "keyword": keyword,
                "score": 5.0,
                "reason": "분석 중 오류가 발생했습니다."
            })
    
    # 점수 기준 내림차순 정렬
    top_trends.sort(key=lambda x: x["score"], reverse=True)
    
    # 상태 업데이트
    state["top_trends"] = top_trends
    
    return state
