from typing import Dict, List, Optional, TypedDict
from typing_extensions import Annotated
from langgraph.graph import add_messages

class TechTrendState(TypedDict):
    # 검색 및 데이터 수집
    search_results: List[Dict]
    
    # 요약 및 분석
    summary: Dict[str, str]  # 검색 결과 요약 정보
    trend_metrics: Dict[str, float]
    
    # 분석 결과
    top_trends: List[Dict]  # 상위 AI 트렌드 목록
    trend_analysis: Dict  # 트렌드 분석 데이터
    
    # 결과 보고서
    report: Optional[str]  # 최종 생성된 트렌드 분석 보고서
    
    # 그래프 제어
    messages: Annotated[List, add_messages]  # 노드 간 커뮤니케이션용 메시지