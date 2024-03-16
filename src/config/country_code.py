import os
import json

COUNTRIES = [
    "대한민국",
    "일본",
    "미국",
    "캐나다",
    "영국",
    "독일",
    "프랑스",
    "인도",
    "러시아",
    "브라질",
    "호주",
    "이탈리아",
    "스페인",
    "멕시코",
    "스웨덴",
    "네덜란드",
    "터키",
    "뉴질랜드",
    "아르헨티나",
    "폴란드",
    "남아프리카 공화국",
]


def country_to_country_code(country):
    with open(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "../../", "data", "country_code.json"
            )
        ),
        "r",
    ) as f:
        country_codes = json.load(f)
    return country_codes[country]
