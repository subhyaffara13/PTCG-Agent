
def _generate_watsonx_token(api_key: Optional[str], token: Optional[str]) -> str:
    if token is not None:
        return token
    token = generate_iam_token(api_key)
    return token

