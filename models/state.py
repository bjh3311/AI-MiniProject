from typing import Dict, List, TypedDict

class TechTrendState(TypedDict):

    # 검색된 키워드 목록
    keywords: List[str] 

    # 검색 및 데이터 수집
    search_results: List[Dict]
    
    # 요약 및 분석
    summary: List[Dict]  # 검색 결과 요약 정보
    
    # 분석 결과
    top_trends: List[Dict]  # 상위 AI 트렌드 목록
    