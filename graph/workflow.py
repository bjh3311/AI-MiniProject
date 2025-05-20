from langgraph.graph import StateGraph

from models.state import TechTrendState
from agents.keywords_agent import extract_keywords
from agents.search_agent import web_search
from agents.summary_agent import summarize_search_results
from agents.analysis_agent import analyze_trends
from agents.report_agent import generate_report

def create_tech_trend_workflow() -> StateGraph:
    """기술 트렌드 분석을 위한 LangGraph 워크플로우 생성"""
    
    # 상태 기반 그래프 초기화
    workflow = StateGraph(TechTrendState)
    
    # 노드 추가
    workflow.add_node("KeywordsSearch", extract_keywords)
    workflow.add_node("WebSearch", web_search)
    workflow.add_node("SearchSummarization", summarize_search_results)
    workflow.add_node("Analysis", analyze_trends)
    workflow.add_node("Report", generate_report)
    
    # 엣지 정의
    workflow.add_edge("WebSearch", "SearchSummarization")
    workflow.add_edge("SearchSummarization", "Analysis")
    workflow.add_edge("Analysis", "Report")
    
    # 시작점과 종료점 설정
    workflow.set_entry_point("WebSearch")
    workflow.set_finish_point("Report")
    
    return workflow.compile()