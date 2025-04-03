import random
import requests
from bs4 import BeautifulSoup

"""Tistory 블로그 텍스트를 .txt 파일로 저장 (p.total 제외)"""

# 검색 결과 페이지 URL
url = "https://miny-genie.tistory.com/"

# 웹페이지 요청
headers = {"User-Agent": "Mozilla/5.0"}

# 1부터 42까지 숫자 중 랜덤으로 10개를 추출
random_numbers = random.sample(range(1, 400), 20)

# 파일 열기 (쓰기 모드)
with open("tistory_texts.txt", "w", encoding="utf-8") as file:
    for i in random_numbers:
        post_url = url + str(i)
        response = requests.get(post_url, headers=headers)

        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, "html.parser")

            # `p` 태그 찾기 (단, class가 "total"인 요소 제외)
            descriptions = [p for p in soup.select("p") if "text-total" not in p.get("class", [])]

            # 텍스트 추출 및 파일 저장
            extracted_texts = [desc.get_text(strip=True) for desc in descriptions if desc.get_text(strip=True)]
            
            if extracted_texts:  # 본문이 존재할 경우에만 저장
                file.write("\n".join(extracted_texts))
                print(f"저장 완료: {post_url}")  # 진행 상황 출력
            else:
                print(f"본문 없음: {post_url}")

        else:
            print(f"요청 실패: {post_url} (Status Code: {response.status_code})")

print("\n크롤링 완료! 'tistory_texts.txt' 파일에 저장됨.")
