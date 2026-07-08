import requests
from exceptions.bot_exceptions import *
import os


def send_request(url):
    nexon_api_key = os.getenv('NEXON_API_KEY')
    if nexon_api_key is None:
        print("넥슨 API가 없음")
        raise RuntimeError("넥슨 API가 없음")

    headers = {
        "x-nxopen-api-key": nexon_api_key
    }
    response = requests.get(url, headers=headers)
    check_error(response=response.json())

    return response.json()


def check_error(response):
    error_json = response.get("error")
    if error_json:
        error_code = error_json.get("name")
        ERRORS = {
            "OPENAPI00001": RuntimeError(),
            "OPENAPI00002": ForbiddenOperation(),
            "OPENAPI00003": InvalidIdentifier("유효하지 않은 식별자"),
            "OPENAPI00004": CharacterNotFound("존재하지 않는 캐릭터입니다"),
            "OPENAPI00005": InvalidApiKey("유효하지 않은 API KEY"),
            "OPENAPI00006": InvalidGame("유효하지 않은 게임 또는 API PATH"),
            "OPENAPI00007": ApiExceed(),
            "OPENAPI00009": IllegalStateException("데이터 준비 중"),
            "OPENAPI00010": GameMaintenance(),
            "OPENAPI00011": ApiMaintenance(),
        }
        if error_code in ERRORS:
            print(f"{error_code} 발생")
            raise ERRORS[error_code]
