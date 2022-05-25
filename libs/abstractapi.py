import os
import requests


def validate_email(email):
    request_url = f'https://emailvalidation.abstractapi.com/v1/?' \
                  f'api_key={os.getenv("EMAILVERIFICATION_ABSTRACTAPI_KEY")}&' \
                  f'email={email}'

    response = requests.get(url=request_url)
    quality_score = float(response.json()['quality_score'])

    return quality_score > 0.5


if __name__ == "__main__":
    validate_email("khantadze.aleko@kiu.edu.ge")
