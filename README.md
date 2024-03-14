# 유튜브 트렌드 대시보드
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=round)](https://makeapullrequest.com)
> 이 프로젝트는 YouTube 인기 동영상 트렌드와 동영상 댓글을 분석하기 위한 웹 애플리케이션을 제공합니다. YouTube Data API v3를 활용하여 다양한 국가의 인기 동영상 순위를 가져와 업로드 패턴, 시청자의 참여도, 동영상 댓글의 감정 분석에 대한 인사이트를 제공합니다. Python으로 구축된 이 애플리케이션은 데이터 조작을 위한 Pandas, 댓글 감정 분석을 위한 TextBlob, 웹 인터페이스를 위한 Streamlit 등의 라이브러리를 활용합니다.

![youtube-trend-dashboard](https://github.com/madEffort/youtube-trend-dashboard/assets/158125247/94104198-0f7c-49d2-8c99-7c37bdb1824b)



## 기능
- **국가 선택:** 사용자는 국가를 선택하여 해당 지역의 인기 YouTube 동영상의 목록을 볼 수 있습니다.
- **인기 동영상 분석**: 정렬 및 페이징 기능이 포함된 인기 동영상 대시보드를 표시합니다.
- **분석 기능:** 요일별 또는 시간별 업로드 비율, 인기 동영상에 사용된 평균 태그 수 등의 분석 기능이 포함되어 있습니다.
- **워드 클라우드 시각화:** 인기 있는 동영상의 제목에서 워드 클라우드를 생성하여 공통 주제 또는 키워드에 대한 시각적 인사이트를 제공합니다.
- **동영상 댓글 분석:** 특정 동영상의 댓글에 대한 감정 분석을 수행하여 긍정, 중립 또는 부정 감정으로 분류합니다.
- **대화형 인터페이스:** 이 애플리케이션은 Streamlit을 사용하는 대화형 인터페이스를 제공하여 사용자가 다양한 분석 및 시각화를 쉽게 탐색할 수 있도록 제공합니다.

## 설치 방법
1. 레포지토리 복제
```
git clone https://github.com/madEffort/youtube-trend-dashboard.git
```
2. 가상환경 생성
3. 필수 패키지 설치
```
pip install -r requirements.txt
```
4. 애플리케이션 실행
```
cd src
streamlit run main.py
```

## 사용 방법
애플리케이션을 실행한 후 왼쪽의 대화형 사이드바를 따라 기능을 탐색합니다:

- 국가를 선택하여 해당 국가의 인기 Youtube 동영상을 확인합니다.
- 분석 옵션을 선택하고 `분석 실행하기`를 클릭하여 분석을 실행합니다.
- 워드클라우드를 생성하려면 `워드클라우드 생성하기` 버튼을 클릭합니다.
- 동영상 댓글 분석을 하려면 YouTube 동영상 ID를 입력하고 `분석하기`를 클릭합니다.

메인 패널에 데이터 시각화 및 댓글 분석 요약을 포함한 결과가 표시됩니다.

## 사용된 기술
- **Python:** 프로젝트의 핵심 프로그래밍 언어
- **Streamlit:** 대화형 웹 애플리케이션을 만드는데 사용
- **Pandas:** 데이터 조작 및 분석에 사용
- **TextBlob:** 동영상 댓글에 대한 감정 분석을 수행
- **YouTube Data API v3:** 인기 동영상 데이터 및 댓글을 가져오는데 사용
- **Matplotlib 및 WordCloud:** 시각화 생성에 사용

이 프로젝트는 모델-뷰-컨트롤러(MVC) 아키텍처 디자인 패턴에 따라 구조화되었습니다.


## 정보

MIT 라이센스를 준수하며 [LICENSE](https://github.com/madEffort/youtube-trend-dashboard/blob/main/LICENSE) 에서 자세한 정보를 확인할 수 있습니다.
