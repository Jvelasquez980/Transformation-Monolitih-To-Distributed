import requests
from flask import request, current_app

AUTH_SERVICE_URL = 'http://auth-service:5000'

def get_logged_user():
    token = request.cookies.get('access_token')

    # print(f"TOKEN ENCONTRADO: {token}", flush=True) 
    if not token:
        return None

    try:
        response = requests.get(
            f'{AUTH_SERVICE_URL}/api/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        current_app.logger.error("No se pudo contactar el auth-service")
        return None


# # utils/auth_helpers.py
# import requests
# from flask import request

# AUTH_SERVICE_URL = 'http://localhost:5000'

# def get_logged_user():
#     token = request.cookies.get('access_token')
#     if not token:
#         return None

#     headers = {'Authorization': f'Bearer {token}'}
#     try:
#         response = requests.get(f'{AUTH_SERVICE_URL}/api/me', headers=headers)
#         if response.status_code == 200:
#             return response.json()
#     except:
#         pass
#     return None
