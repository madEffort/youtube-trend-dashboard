import requests

LOADING = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"


def loading_wait():
    r = requests.get(LOADING)
    if r.status_code != 200:
        return None
    return r.json()
