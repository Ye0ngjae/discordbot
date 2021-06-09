'''

[NiPy]

대부분의 코드에는 주석이 포함되어 있습니다.
Github 문서와 주석을 참고하여 필요한 코드만 살려
경량화 하시기 바랍니다.

'''

# ~~ 0. 임포트 부분 ~~
import requests  # (필수) 나이스 서버와 통신용
import json  # (필수) api 사용시 파싱용
from bs4 import BeautifulSoup  # (필수) 나이스 페이지 파싱용

# ~~ 1. 학교 코드를 불러오는 api ~~

class Scode:  # Scode 클래스 생성
    def __init__(self, name, city):  # 학교 이름과 위치를 받아옴
        city_dict = {"인천": "2800000000"}  # 지역 목록

        self.city = city_dict.get(city, "")  # 지역 코드로 변환
        self.name = name  # 학교 이름 저장

    def codefind(self, kind):  # 실질적으로 코드를 반환하는 부분
        url = "https://www.schoolinfo.go.kr/ei/ss/Pneiss_a01_l0.do"  # 학교알리미 코드 불러오는 주소
        para = {
            "HG_CO": "",
            "SEARCH_KIND": "",
            "HG_JONGRYU_GB": "",
            "GS_HANGMOK_CD": "",
            "GU_GUN_CODE": "",
            "GUGUN_CODE": "",
            "SIDO_CODE": self.city,
            "SRC_HG_NM": self.name
        }  # post 파라미터
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }  # 헤더 데이터

        re = requests.post(url, data=para, headers=headers, verify=False)  # 서버 접속
        rejs = json.loads(re.text)  # json 데이터 불러오기
        reco = re.status_code  # 응답코드 저장

        if int(reco) != 200:
            return("SERVER ERROR")  # 접속 여부 확인

        middle = rejs['schoolList03']  # 중학교 데이터

        if len(elementary) == 0 and len(middle) == 0 and len(high) == 0 and len(special) == 0:
            return("CAN NOT FIND SCHOOL")

        # 담아서 넘길 리스트 만들기
        self.elementary = []
        self.middle = []
        self.high = []
        self.special = []

        if len(middle) > 0:  # 중학교 데이터 분석
            for i in range(0, len(middle)):
                sinfo = middle[i]
                sname = sinfo['SCHUL_NM']
                saddress = sinfo['SCHUL_RDNMA']
                sncode = sinfo['SCHUL_CODE']

                sinfo = {
                    'NAME': sname,
                    'ADDRESS': saddress,
                    'CODE': sncode
                }

                self.middle.append(sinfo)


        if kind == "2":
            slist = self.middle
        else:
            slist = [self.elementary, self.middle, self.high, self.special]

        return(slist)

 # ~~ 2. 학교 급식을 불러오는 api ~~


# ~~ 2. 학교 급식을 불러오는 api ~~

class Smeal:  # Smeal 클래스 생성
    def __init__(self, ooe, code, sclass):  # 초기화자 메서드 선언 (기본학교정보설정)
        city_dict = {"인천": "ice.go.kr"}  # 학교 목록

        self.ooe = city_dict.get(ooe, "nocity")
        self.sclass = sclass  # 교급
        self.code = code  # 학교 고유 코드

    def day(self, yeon, dal, il, kind):  # 하루치 급식을 조회

        ymd = yeon + "." + dal + "." + il  # 년도 조합

        url = "http://stu." + self.ooe + "/sts_sci_md01_001.do"  # 나이스 급식 조회 주소
        para = {
            "schulCode": self.code,  # 학교 코드
            "schulCrseScCode": self.sclass,  # 교급
            "schulKnaScCode": "0" + self.sclass,  # 교급
            "schMmealScCode": kind,  # 식단 종류
            "schYmd": ymd  # 조회년월일
        }

        response = requests.get(url, params=para)  # 급식 정보 조회
        if int(response.status_code) != 200:  # 응답이 200 (정상응답)이 아닐경우
            return('SERVER ERROR')  # 에러 반환

        foodhtml = BeautifulSoup(response.text, 'html.parser')  # 급식정보 파싱 준비
        foodhtml_data_tr = foodhtml.find_all('tr')  # 모든 tr태그 불러오기

        # 몇번째 행에 급식 정보가 존재하는지 구분하는 로직

        foodhtml_data = foodhtml_data_tr[0].find_all('th')  # 날짜 정보가 있는 열을 불러옴

        try:  # 예외 처리를 위한 try
            for i in range(1, 7):  # 월요일부터 일요일까지 하나하나 대입 준비
                date = str(foodhtml_data[i])  # i요일째 날짜 정보 확인
                date_filter = ['<th class="point2" scope="col">', '<th class="last point1" scope="col">',
                               '<th scope="col">', '</th>', '(', ')', '일', '월', '화', '수', '목', '금', '토']  # 제거해야 하는 목록

                for sakje in date_filter:
                    date = date.replace(sakje, '')  # 찌끄레기를 삭제

                if date != ymd:  # 날짜와 입력날짜 동일 여부 확인
                    continue

                hang = i - 1  # 급식정보가 존재하는 행 선언
                break  # 존재 확인 로직 정지

        except:  # 에러 발생시 데이터베이스 에러 반환
            return("NO DATABASE")

        # 급식 정보 조회 시작

        try:
            food = foodhtml_data_tr[2].find_all(
                'td')  # 급식정보가 있는 행의 모든 td 태그 불러오기
            food = str(food[hang])  # hang 번째에 있는 급식 정보 불러옴

            food_filter = ['<td class="textC">',
                           '<td class="textC last">', '</td>']  # 제거해야 하는 목록

            for sakje in food_filter:
                food = food.replace(sakje, '')  # 찌끄레기를 삭제

            if food == ' ':
                food = '급식이 예정되지 않았거나 정보가 존재하지 않습니다.'  # 만약 조회시 급식정보가 없다면 미존재 안내

        except:
            food = 'NO DATABASE'  # 급식 조회 실패시 안내

        return(food)  # 정보 반환

   


# ~~ 3. 학교 학사일정을 불러오는 api ~~

class Scalendar:  # Scalendar 클래스 생성
    def __init__(self, ooe, code, sclass):  # 초기화자 선언
        city_dict = {"인천": "ice.go.kr"}  # 학교 목록

        self.ooe = city_dict.get(ooe, "nocity")
        self.sclass = sclass  # 교급
        self.code = code  # 학교 고유 코드

    def month(self, yeon, dal):

        try:
            url = "http://stu." + self.ooe + "/sts_sci_sf01_001.do"  # 월간 계획 주소
            para = {
                "schulCode": self.code,  # 학교코드
                "schulCrseScCode": self.sclass,  # 교급
                "schulKndScCode": "0" + self.sclass,  # 교급
                "ay": yeon,  # 조회년도
                "mm": dal  # 조회월
            }

            re = requests.get(url, params=para)  # 나이스 학사일정 조회
            if int(re.status_code) != 200:  # 비정상 접속시 에러 반환
                return("SERVER ERROR")

            html = BeautifulSoup(re.text, 'html.parser')  # 파싱 준비
            html = html.find_all('td')  # td(테이블 구분) 태그만 불러옴

            html_size = len(html)  # 몇줄 있는지 확인
            calendar = {}

            for i in range(0, html_size):  # 날짜 및 일정 내용 분류
                html_date = str(html[i].find('em'))  # 날짜 정보 빼오기
                html_body = str(html[i].find('strong'))  # 일정 정보 빼오기

                for sakje in ['<em>', '</em>', '<em class="point2">']:
                    html_date = html_date.replace(sakje, '')  # html 태그 제거

                for sakje in ['<strong>', '</strong>']:
                    html_body = html_body.replace(sakje, '')  # html 태그 제거

                if html_body == "None":  # 학사일정 미 존재시
                    html_body = "학사일정이 존재하지 않습니다."  # 안내멘트

                if html_date == "":  # 날짜정보 미 존재시
                    continue  # 반복문 탈출

                calendar[html_date] = html_body  # 딕셔너리 추가

        except:
            calendar = "NO DATABASE"  # 에러 전달

        return(calendar)  # 반환
