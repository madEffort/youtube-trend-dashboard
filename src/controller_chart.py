def generate_dayofweek_chart(data):
    chart = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {
            "type": "category",
            "data": [
                "월요일",
                "화요일",
                "수요일",
                "목요일",
                "금요일",
                "토요일",
                "일요일",
            ],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": [int(data.iloc[i]["업로드 수"]) for i in range(len(data))],
                "type": "bar",
            }
        ],
    }
    return chart


def generate_timebyday_chart(data):
    chart = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {
            "type": "category",
            "data": [str(i) + "시" for i in range(len(data))],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": [int(data.iloc[i]) for i in range(len(data))],
                "type": "bar",
            }
        ],
    }
    return chart


def generate_pie_chart(data, option):
    chart = {
        "title": {
            "text": f"{option} 비교 차트",
            "tooltip": {"trigger": "item"},
            "left": "center",
        },
        "tooltip": {
            "trigger": "item",
            "formatter": "{a} <br/>{b}: {c} ({d}%)",
        },
        "series": [
            {
                "name": f"{option}",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": int(data[0][option]), "name": f"{data[0]['채널명']}"},
                    {"value": int(data[1][option]), "name": f"{data[1]['채널명']}"},
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }
    return chart
