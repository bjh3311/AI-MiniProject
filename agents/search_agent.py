from typing import Dict
from langchain_community.utilities import SerpAPIWrapper

def web_search(state: Dict) -> Dict:
    """WebSearch 노드 - 미래 AI 기술 트렌드에 대한 정보 검색"""
    
    # 검색 엔진 초기화
    search = SerpAPIWrapper()
    
    # 검색 쿼리 정의
    search_queries = [
        "최신 AI 기술 트렌드",
        "향후 5년 AI 발전 전망",
        "유망한 인공지능 기술",
        "산업 분야 AI 연구 동향",
        "AI 투자 트렌드",
        "기업의 AI 도입 사례"
    ]
    
    # 검색 수행
    results = []
    for query in search_queries:
        search_result = search.run(query)
        results.append({
            "query": query,
            "result": search_result
        })
    
    # 상태 업데이트
    return {"search_results": results}