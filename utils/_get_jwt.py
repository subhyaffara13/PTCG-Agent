
def _get_jwt(auth_url, api_id, api_key):
    token_url = f"{auth_url}/oauth2/token?grant_type=client_credentials"

    resp = requests.post(token_url, auth=HTTPBasicAuth(api_id, api_key))

    if not resp.ok:
        raise RuntimeError(
            f"Unable to get authentication credentials for the HiddenLayer API: {resp.status_code}: {resp.text}"
        )

    if "access_token" not in resp.json():
        raise RuntimeError(
            f"Unable to get authentication credentials for the HiddenLayer API - invalid response: {resp.json()}"
        )

    return resp.json()["access_token"]

