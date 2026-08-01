
def _load_client() -> OpenAI:  # type: ignore[reportUnusedFunction]
    global _client

    if _client is None:
        global api_type, azure_endpoint, azure_ad_token, api_version

        if azure_endpoint is None:
            azure_endpoint = _os.environ.get("AZURE_OPENAI_ENDPOINT")

        if azure_ad_token is None:
            azure_ad_token = _os.environ.get("AZURE_OPENAI_AD_TOKEN")

        if api_version is None:
            api_version = _os.environ.get("OPENAI_API_VERSION")

        if api_type is None:
            has_openai = _has_openai_credentials()
            has_azure = _has_azure_credentials()
            has_azure_ad = _has_azure_ad_credentials()

            if has_openai and (has_azure or has_azure_ad):
                raise _AmbiguousModuleClientUsageError()

            if (azure_ad_token is not None or azure_ad_token_provider is not None) and _os.environ.get(
                "AZURE_OPENAI_API_KEY"
            ) is not None:
                raise _AmbiguousModuleClientUsageError()

            if has_azure or has_azure_ad:
                api_type = "azure"
            else:
                api_type = "openai"

        if api_type == "azure":
            _client = _AzureModuleClient(  # type: ignore
                api_version=api_version,
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                azure_ad_token=azure_ad_token,
                azure_ad_token_provider=azure_ad_token_provider,
                organization=organization,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
                default_query=default_query,
                http_client=http_client,
            )
            return _client

        if api_type == "amazon-bedrock":
            _client = _BedrockModuleClient(  # type: ignore
                api_key=api_key,
                bedrock_token_provider=bedrock_token_provider,
                organization=organization,
                project=project,
                webhook_secret=webhook_secret,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
                default_query=default_query,
                http_client=http_client,
            )
            return _client

        _client = _ModuleClient(
            api_key=api_key,
            admin_api_key=admin_api_key,
            organization=organization,
            project=project,
            webhook_secret=webhook_secret,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _enforce_credentials=False,
        )
        return _client

    return _client

