import re
from typing import Dict, List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


def extract_keywords(state: Dict) -> Dict:
    """
    LLM을 사용하여 향후 5년 이내 기업이 관심을 가져야 할 AI 트렌드 키워드 5개를 생성하는 함수
    LangGraph의 노드로 동작하며, TechTrendState의 keywords 필드를 업데이트합니다.
    """
    # LLM 모델 초기화 (OpenAI 모델 사용)
    llm = ChatOpenAI(temperature=0.1, model="gpt-4")    
    # LLM에게 AI 트렌드 키워드 생성 요청
    prompt = """
    너가 생각하는 향후 5년 이내 기업에서 관심있게 봐야할 AI 트랜드 키워드 10개를 만들어서 단어 리스트로 보여줘.
    
    다음 규칙을 따라 응답해주세요:
    1. 최신 AI 트렌드와 미래 유망 기술에 초점을 맞추세요
        1 - 1. 대신 단순하게 AI 보안, AI 윤리, AI 규제와 같이 AI에 다른 단어를 합성한 것으로는 안됩니다
        1 - 2. 너무 일반적인 단어는 피해주세요 (예: AI, 머신러닝, 딥러닝 등)
    2. 키워드는 1-3개 단어로 간결하게 표현해주세요
    3. 응답은 각 키워드를 줄바꿈으로 구분하여 제공하세요 (예: "단어1\n단어2\n단어3")
    4. 키워드 앞에 번호를 붙이지 마세요
    5. 설명이나 추가 문장 없이 키워드만 제공해주세요
    """
    
    response = llm.invoke(prompt)
    response_text = response.content
    
    # 응답에서 키워드 목록 추출
    # 줄바꿈으로 구분된 문자열을 분리하고 공백을 제거
    keywords = [keyword.strip() for keyword in response_text.split('\n') if keyword.strip()]
    
    # 중복 제거 및 최대 15개로 제한
    unique_keywords = list(dict.fromkeys(keywords))
    final_keywords = unique_keywords[:10]

    # state 업데이트
    state["keywords"] = final_keywords
    
    return state