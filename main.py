from graph.workflow import create_tech_trend_workflow
from models.state import TechTrendState
import json
import os
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
        search_results=[],
        summary={},
        trend_metrics={},
        top_trends=[],
        trend_analysis={},
        report=None,
        messages=[]
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
            
            # 최종 보고서 저장
            final_state = event["Report"]
            report = final_state.get("report", "보고서가 생성되지 않았습니다")
            
            with open("tech_trend_report.md", "w", encoding="utf-8") as f:
                f.write(report)
            
            logger.info(f"보고서가 tech_trend_report.md에 저장되었습니다")
            
            # 디버깅용 전체 상태 저장
            with open("tech_trend_state.json", "w", encoding="utf-8") as f:
                # 직렬화 가능한 형식으로 변환
                serializable_state = {
                    k: v for k, v in final_state.items() if k != "messages"
                }
                json.dump(serializable_state, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()