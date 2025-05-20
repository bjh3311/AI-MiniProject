import requests
from typing import List
import os
from dotenv import load_dotenv


# .env 파일 로드
load_dotenv()

def get_naver_news_links(query: str, num_links: int = 100) -> List[str]:
    """
    네이버 뉴스 API를 사용하여 특정 키워드에 대한 뉴스 링크를 가져옵니다.
    """
    client_id = os.getenv('NAVER_CLIENT_ID')
    client_secret = os.getenv('NAVER_CLIENT_SECRET')
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={num_links}&sort=sim"
    headers = {
        'X-Naver-Client-Id': client_id,  # 네이버 API 클라이언트 ID
        'X-Naver-Client-Secret': client_secret  # 네이버 API 클라이언트 Secret
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"네이버 API 요청 실패: {response.status_code}, {response.text}")
    
    result = response.json()
    filtered_links = []
    for item in result['items']:
        link = item['link']
        if "n.news.naver.com/mnews/article/" in link:  # 네이버 뉴스 형식 필터링
            filtered_links.append(link)
    
    return filtered_links

# 테스트 실행
if __name__ == "__main__":
    topics = ['LLM', '생성 인공지능', 'GPT', '딥러닝', '가전제품']
    all_links = []
    for topic in topics:
        all_links += get_naver_news_links(topic, 10)
    
    # 중복 제거
    unique_links = list(set(all_links))
    print(f"총 {len(all_links)}개의 뉴스 링크를 가져왔습니다.")