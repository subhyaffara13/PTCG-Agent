from typing import Optional

def generate_iam_token(api_key=None, **params) -> str:
    result: Optional[str] = iam_token_cache.get_cache(api_key)  # type: ignore

    if result is None:
        headers = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        if api_key is None:
            api_key = (
                get_secret_str("WX_API_KEY")
                or get_secret_str("WATSONX_API_KEY")
                or get_secret_str("WATSONX_APIKEY")
                or get_secret_str("WATSONX_ZENAPIKEY")
            )
        if api_key is None:
            raise ValueError("API key is required")
        headers["Accept"] = "application/json"
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key,
        }
        iam_token_url = get_watsonx_iam_url()
        verbose_logger.debug(
            "calling ibm `/identity/token` to retrieve IAM token.\nURL=%s\nheaders=%s\ndata=%s",
            iam_token_url,
            headers,
            data,
        )
        response = litellm.module_level_client.post(
            url=iam_token_url, data=data, headers=headers
        )
        response.raise_for_status()
        json_data = response.json()

        result = json_data["access_token"]
        iam_token_cache.set_cache(
            key=api_key,
            value=result,
            ttl=json_data["expires_in"] - 10,  # leave some buffer
        )

    return cast(str, result)

