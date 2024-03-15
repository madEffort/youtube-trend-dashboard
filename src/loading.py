import requests

# 로딩 중 애니메이션의 URL
LOADING = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"

def loading_wait():
    """
    로딩 중일 때 사용자에게 보여줄 애니메이션을 가져오는 함수입니다.
    """
    r = requests.get(LOADING)  # 로딩 애니메이션을 가져옵니다.
    if r.status_code != 200:
        return None
    return r.json()  # 가져온 애니메이션을 JSON 형식으로 반환합니다.