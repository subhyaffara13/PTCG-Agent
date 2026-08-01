
def get_api_key(llm_provider: str, dynamic_api_key: Optional[str]):
    api_key = dynamic_api_key or litellm.api_key
    # openai
    if llm_provider == "openai" or llm_provider == "text-completion-openai":
        api_key = api_key or litellm.openai_key or get_secret("OPENAI_API_KEY")
    # anthropic
    elif llm_provider == "anthropic" or llm_provider == "anthropic_text":
        api_key = api_key or litellm.anthropic_key or get_secret("ANTHROPIC_API_KEY")
    # ai21
    elif llm_provider == "ai21":
        api_key = api_key or litellm.ai21_key or get_secret("AI211_API_KEY")
    # aleph_alpha
    elif llm_provider == "aleph_alpha":
        api_key = (
            api_key or litellm.aleph_alpha_key or get_secret("ALEPH_ALPHA_API_KEY")
        )
    # baseten
    elif llm_provider == "baseten":
        api_key = api_key or litellm.baseten_key or get_secret("BASETEN_API_KEY")
    # cohere
    elif llm_provider == "cohere" or llm_provider == "cohere_chat":
        api_key = api_key or litellm.cohere_key or get_secret("COHERE_API_KEY")
    # huggingface
    elif llm_provider == "huggingface":
        api_key = (
            api_key or litellm.huggingface_key or get_secret("HUGGINGFACE_API_KEY")
        )
    # nlp_cloud
    elif llm_provider == "nlp_cloud":
        api_key = api_key or litellm.nlp_cloud_key or get_secret("NLP_CLOUD_API_KEY")
    # replicate
    elif llm_provider == "replicate":
        api_key = api_key or litellm.replicate_key or get_secret("REPLICATE_API_KEY")
    # together_ai
    elif llm_provider == "together_ai":
        api_key = (
            api_key
            or litellm.togetherai_api_key
            or get_secret("TOGETHERAI_API_KEY")
            or get_secret("TOGETHER_AI_TOKEN")
        )
    # nebius
    elif llm_provider == "nebius":
        api_key = api_key or litellm.nebius_key or get_secret("NEBIUS_API_KEY")
    # wandb
    elif llm_provider == "wandb":
        api_key = api_key or litellm.wandb_key or get_secret("WANDB_API_KEY")
    return api_key


def get_api_key(
    custom_litellm_key_header: Optional[str],
    api_key: str,
    azure_api_key_header: Optional[str],
    anthropic_api_key_header: Optional[str],
    google_ai_studio_api_key_header: Optional[str],
    azure_apim_header: Optional[str],
    pass_through_endpoints: Optional[List[dict]],
    route: str,
    request: Request,
) -> Tuple[str, Optional[str]]:
    """
    Returns:
        Tuple[Optional[str], Optional[str]]: Tuple of the api_key and the passed_in_key
    """
    from litellm.proxy.auth.route_checks import RouteChecks
    from litellm.proxy.common_utils.http_parsing_utils import (
        _safe_get_request_query_params,
    )

    api_key = api_key
    passed_in_key: Optional[str] = None
    if isinstance(custom_litellm_key_header, str):
        passed_in_key = custom_litellm_key_header
        api_key = _get_bearer_token_or_received_api_key(custom_litellm_key_header)
    elif isinstance(api_key, str) and len(api_key) > 0:
        passed_in_key = api_key
        api_key = _get_bearer_token(api_key=api_key)
    elif isinstance(azure_api_key_header, str):
        passed_in_key = azure_api_key_header
        api_key = azure_api_key_header
    elif isinstance(anthropic_api_key_header, str):
        passed_in_key = anthropic_api_key_header
        api_key = anthropic_api_key_header
    elif isinstance(google_ai_studio_api_key_header, str):
        passed_in_key = google_ai_studio_api_key_header
        api_key = google_ai_studio_api_key_header
    elif isinstance(azure_apim_header, str):
        passed_in_key = azure_apim_header
        api_key = azure_apim_header
    elif (
        RouteChecks.is_generate_content_route(route=route)
        and request is not None
        and _safe_get_request_query_params(request).get("key")
    ):
        google_auth_key: str = _safe_get_request_query_params(request).get("key") or ""
        passed_in_key = google_auth_key
        api_key = google_auth_key
    elif pass_through_endpoints is not None:
        for endpoint in pass_through_endpoints:
            if endpoint.get("path", "") == route:
                headers: Optional[dict] = endpoint.get("headers", None)
                if headers is not None:
                    header_key: str = headers.get("litellm_user_api_key", "")
                    if request.headers.get(header_key) is not None:
                        api_key = request.headers.get(header_key) or ""
                        passed_in_key = api_key
    return api_key, passed_in_key

