import requests

url = "https://shadedoes3d.com/api/auth"


def sda_login(username, password):
    # A GET request to the API
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    json_resp = response.json()
    if json_resp.get('status', 'failure') != 'success':
        return False, None

    token = json_resp.get('data').get('token')
    user_data = requests.get("https://shadedoes3d.com/api/users/me", headers={
        "Authorization": f"Token {token}"
    }).json()
    return True, user_data.get('data')
    # save data if necessary
    pass
