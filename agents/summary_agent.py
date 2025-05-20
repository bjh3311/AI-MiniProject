from typing import Dict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def summarize_search_results(state: Dict) -> Dict:
    """
    Search Summarization 노드 - 검색 결과 요약
    각 키워드별로 뉴스 본문을 요약합니다.
    """
    # 검색 결과가 없으면 빈 요약 반환
    if not state.get("search_results"):
        return state
    
    # LLM 초기화
    llm = ChatOpenAI(temperature=0.1, model="gpt-4")
    
    summaries = []
    
    # 각 키워드별로 개별 요약 생성
    for result in state.get("search_results", []):
        keyword = result.get("keyword", "")
        content = result.get("content", "")
        
        if not keyword or not content:
            continue
        
        # content를 일정 길이로 분할
        max_chunk_size = 3000  # 토큰 수를 고려하여 적절히 설정
        content_chunks = [content[i:i+max_chunk_size] for i in range(0, len(content), max_chunk_size)]
        
        # 각 chunk를 요약
        chunk_summaries = []
        for chunk in content_chunks:
            summary_prompt = f"""
            다음 키워드 '{keyword}'에 관한 뉴스 기사 본문 일부가 주어집니다. 이 내용을 객관적으로 요약해주세요.
            
            요약 시 다음 사항을 준수해주세요:
            1. 1500단어 이내로 간결하게 요약하세요.
            2. 본문에 없는 추가적인 의견이나 분석을 포함하지 마세요.
            3. 객관적 사실만 요약하세요.
            4. 내용의 핵심 주제와 중요 정보를 포함하세요.
            
            뉴스 본문:
            {chunk}
            
            요약:
            """
            
            # 요약 생성
            summary_response = llm.invoke(summary_prompt)
            chunk_summary = summary_response.content.strip()
            chunk_summaries.append(chunk_summary)
        
        # 모든 chunk 요약을 합쳐 최종 요약 생성
        final_summary = " ".join(chunk_summaries)
        
        # 요약 결과 저장
        summaries.append({
            "keyword": keyword,
            "summary": final_summary
        })
        for item in summaries:
            print(f"키워드: {item['keyword']}, 요약: {item['summary']}")
    
    # 상태 업데이트
    state["summary"] = summaries
    return state