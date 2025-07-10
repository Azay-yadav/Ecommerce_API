import requests
from django.conf import settings

def get_paypal_access_token():
    url = f"{settings.PAYPAL_API_BASE}/v1/oauth2/token"
    response = requests.post(
        url,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
        data={'grant_type': 'client_credentials'},
    )
    response.raise_for_status()
    return response.json()['access_token']
