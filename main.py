from graph.workflow import create_tech_trend_workflow
from models.state import TechTrendState
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """기술 트렌드 분석 애플리케이션의 메인 엔트리 포인트"""
    
    
    # 워크플로우 생성
    tech_trend_workflow = create_tech_trend_workflow()
    
    # 초기 상태 설정
    initial_state = TechTrendState(
        keywords = [], 
        search_results = [],
        summary = [],
        top_trends = []
    )
    
    # 워크플로우 실행
    for event in tech_trend_workflow.stream(initial_state):
        if "WebSearch" in event:
            logger.info("✅ 웹 검색 완료")
        elif "SearchSummarization" in event:
            logger.info("✅ 검색 결과 요약 완료")
        elif "Analysis" in event:
            logger.info("✅ 트렌드 분석 완료")
        elif "Report" in event:
            logger.info("✅ 최종 보고서 생성 완료")

if __name__ == "__main__":
    main()