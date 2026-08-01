
def _assert_provider_owns_authorization(request: httpx.Request) -> None:
    if "Authorization" in request.headers:
        raise OpenAIError("Bedrock provider authentication cannot be combined with a custom `Authorization` header.")

