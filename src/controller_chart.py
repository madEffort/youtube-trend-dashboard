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

