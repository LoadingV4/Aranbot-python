import requests
from exceptions.bot_exceptions import *
import os


def nexon_request(url):
    nexon_api_key = os.getenv('NEXON_API_KEY')
    if nexon_api_key is None:
        print("넥슨 API가 없음")
        raise RuntimeError("넥슨 API가 없음")
    
    headers = {
        "x-nxopen-api-key": nexon_api_key
    }
    print(f"url : {url}")
    response = requests.get(url, headers=headers)
    print(response.json())
    try:
        check_error(response=response.json())
    except RuntimeError:
        pass
    except ForbiddenOperation:
        pass
    except InvalidIdentifier:
        pass
    except CharacterNotFound:
        pass
    except InvalidApiKey:
        pass

    return response


def check_error(response):
    error_code = response.get("name")
    if error_code:
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
            raise ERRORS[error_code]
