
def _get_mocked_oauth_info() -> dict:
    token = get_token()
    if token is None:
        raise ValueError(
            "Your machine must be logged in to HF to debug an OAuth app locally. Please"
            " run `hf auth login` or set `HF_TOKEN` as environment variable "
            "with one of your access token. You can generate a new token in your "
            "settings page (https://huggingface.co/settings/tokens)."
        )

    user = whoami()
    if user["type"] != "user":
        raise ValueError(
            "Your machine is not logged in with a personal account. Please use a "
            "personal access token. You can generate a new token in your settings page"
            " (https://huggingface.co/settings/tokens)."
        )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 8 * 60 * 60,  # 8 hours
        "id_token": "FOOBAR",
        "scope": "openid profile",
        "refresh_token": "hf_oauth__refresh_token",
        "expires_at": int(time.time()) + 8 * 60 * 60,  # 8 hours
        "userinfo": {
            "sub": "0123456789",
            "name": user["fullname"],
            "preferred_username": user["name"],
            "profile": f"https://huggingface.co/{user['name']}",
            "picture": user["avatarUrl"],
            "website": "",
            "aud": "00000000-0000-0000-0000-000000000000",
            "auth_time": 1691672844,
            "nonce": "aaaaaaaaaaaaaaaaaaa",
            "iat": 1691672844,
            "exp": 1691676444,
            "iss": "https://huggingface.co",
        },
    }

