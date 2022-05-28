import os
import requests


def validate_email(email):
    request_url = f'https://emailvalidation.abstractapi.com/v1/' \
                  f'?api_key={os.getenv("EMAILVERIFICATION_ABSTRACTAPI_KEY")}' \
                  f'&email={email}'

    response = requests.get(url=request_url)
    deliverable = response.json()['deliverability']

    return deliverable in ['DELIVERABLE', 'RISKY']


def get_holiday(country, year, month, day):
    request_url = f'https://holidays.abstractapi.com/v1/' \
                  f'?api_key={os.getenv("HOLIDAYS_ABSTRACTAPI_KEY")}' \
                  f'&country={country}' \
                  f'&year={year}' \
                  f'&month={month}' \
                  f'&day={day}'
    response = requests.get(url=request_url)
    return response.json()


def get_geolocation(ip_address):
    request_url = f'https://ipgeolocation.abstractapi.com/v1/' \
                  f'?api_key={os.getenv("GEOLOCATION_ABSTRACTAPI_KEY")}' \
                  f'&ip_address={ip_address}'
    response = requests.get(url=request_url)
    data = response.json()

    return data if data.get("country", None) else None
