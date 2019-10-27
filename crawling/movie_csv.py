import requests
from bs4 import BeautifulSoup as bs
import openpyxl
import csv
import pandas as pd

'''
(참고) 영화관련정보 엑셀(xlsx)형식 저장 컬럼 목록
    1) 영화제목
    2) 영화평점
    3) 영화장르
    4) 영화감독
    5) 영화배우
    6) 영화포스터
'''
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["영화제목", "영화평점", "영화장르", "영화감독", "영화배우", "영화포스터"])

# (0) HTML 파싱
raw = requests.get("https://movie.naver.com/movie/running/current.nhn", headers={'User-Agent': 'Mozilla/5.0'})
html = bs(raw.text, 'html.parser')

# (1) 전체 컨테이너
movie = html.select("div.lst_wrap li")
with open('test.csv', 'w', encoding='euc-kr', newline='') as writer_csv:
    # (2) 전체 컨테이너가 갖고 있는 영화관련 정보
    for i, m in enumerate(movie):
        # (3-1) 영화제목 수집
        title = m.select_one("dt.tit a")
        # (3-2) 영화평점 수집
        score = m.select_one("div.star_t1 span.num")

        '''
           (참고) select + nth-of-type 문법 활용(부모 속성에서 특정 태그를 가진 자식 속성에서 몇번째 해당하는지의 )
               -> select_one 아니라, select를 써야 여러개 혹은 여러명의 영화장르/영화감독/영화배우 리스트를 가져 오게 됩니다.
        '''

        # (3-3) 영화장르 수집
        genre = m.select("dl.info_txt1 dd:nth-of-type(1) a")

        # (3-4) 영화감독 수집
        directors = m.select("dl.info_txt1 dd:nth-of-type(2) a")

        # (3-5) 영화배우 수집
        actors = m.select("dl.info_txt1 dd:nth-of-type(3) a")

        '''
           (참고) 고급 검색 활용
               -> if/else 문을 이용한 여러가지 명제들을 활용하면, 사용자가 임의로 원하는 데이터만 필터링 할 수 있습니다.
        '''
        # (4) skip 처리-1: 평점이 8.5보다 작으면 넘어간다.
        #     if float(score.text) < 8.5:
        #         continue

        # (5) skip 처리-2 : 장르에 "액션"이 포함되어 있지 않으면 넘어간다.
        #     genre_all = m.select_one("dl.info_txt1 dd:nth-of-type(1) span.link_txt")
        #     if "액션" not in genre_all.text:
        #         continue

        '''
           (참고) Standard Output(일반 출력)
               -> 출력을 보기 쉽게 만들어주는 것은 데이터 수집 확인용을 위해 중요합니다.
        '''
        # (6) ~~~~~ 이쁘게 출력 ~~~~~~~
        print("=" * 50)
        print("제목:", title.text)

        print("=" * 50)
        print("평점:", score.text)

        print("=" * 50)
        print("장르:")
        for g in genre:
            print(g.text)

        print("=" * 50)
        print("감독:")
        for d in directors:
            print(d.text)

        print("=" * 50)
        print("배우:")
        for a in actors:
            print(a.text)

        # (7) 영화관련정보 엑셀(xlsx) 형식 저장
        # (7-1) 데이터 만들기-1 : HTML로 가져온 영화장르/영화감독/영화배우 정보에서 TEXT정보만 뽑아서 리스트 형태로 만들기
        genre_list = [g.text for g in genre]
        directors_list = [d.text for d in directors]
        actors_list = [a.text for a in actors]

        # (7-2) 데이터 만들기-2 : 여러 개로 이루어진 리스트 형태를 하나의 문자열 형태로 만들기
        genre_str = ','.join(genre_list)
        directors_str = ','.join(directors_list)
        actors_str = ','.join(actors_list)

        # (7-3) 영화관련정보 엑셀 행 추가 : line by line 으로 추가하기
        #ataf = {'제목':title_text, '점수':score}
        #DF = pd.DataFrame([title.text, score.text, genre_str, directors_str, actors_str])
        fields = ['first', 'second', 'third']

        writer = csv.writer(writer_csv, delimiter=',')
        writer.writerow([title.text, score.text, genre_str, directors_str, actors_str])
