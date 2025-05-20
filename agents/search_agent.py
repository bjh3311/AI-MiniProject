import requests
from typing import List, Dict
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup


# .env 파일 로드
load_dotenv()


def web_search(state: Dict) -> Dict:
    """
    WebSearch 노드 - 네이버 뉴스 API를 사용하여 특정 키워드에 대한 뉴스 링크를 가져옵니다.
    """
    keywords = state.get("keywords")
    if keywords is None:
        raise Exception("검색할 키워드가 없습니다.")
    # .env 파일에서 환경 변수 가져오기
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise Exception("NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET이 설정되지 않았습니다.")
    
    num_links = 2 # 가져올 뉴스의 개수
    search_results = []

    # 각 키워드에 대해 네이버 뉴스 API를 호출하여 링크를 가져오고 본문을 넣는다
    for query in keywords:
        # 네이버 뉴스 API 요청
        url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={num_links}&sort=sim"
        headers = {
            'X-Naver-Client-Id': client_id,  # 네이버 API 클라이언트 ID
            'X-Naver-Client-Secret': client_secret  # 네이버 API 클라이언트 Secret
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"네이버 API 요청 실패: {response.status_code}, {response.text}")
        
            # 검색 결과 처리
        result = response.json()
        filtered_links = []
        for item in result['items']:
            link = item['link']
            if "n.news.naver.com/mnews/article/" in link:  # 네이버 뉴스 형식 필터링
                filtered_links.append({
                    "query": query,
                    "link": link
                })

        for link in filtered_links:
            # 링크에서 기사 본문 추출
            content = get_news_content(link["link"])
            # 기존에 동일한 keyword가 있는지 확인
            existing_entry = next((item for item in search_results if item["keyword"] == link["query"]), None)
    
            if existing_entry:
                # 기존 keyword가 있다면 content를 추가
                existing_entry["content"] += content
            else:
                # 기존 keyword가 없으면 새로 추가
                search_results.append({
                "keyword": link["query"],
                "content": content
            })
                
    state["search_results"] = search_results        
    # 상태 업데이트
    return state

def get_news_content(link: str) -> str:
    """
    네이버 뉴스 링크에서 뉴스 본문을 추출합니다.
    """
    news_contents = ""
    response = requests.get(link)
    if response.status_code != 200:
        raise Exception(f"뉴스 요청 실패: {response.status_code}, {response.text}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    # 네이버 뉴스 본문 추출 (HTML 구조에 따라 class 이름이 다를 수 있음)
    content = soup.find("div", class_="newsct_body")  # 본문 클래스 이름
    if content:
        news_contents = content.get_text(strip = True)
    else:
        raise Exception(f"본문을 찾을 수 없음: {link}")
    
    return news_contents
