
def get_anthropic_config(
    url_route: str,
) -> Union[Type[AnthropicBatchesConfig], Type[AnthropicConfig]]:
    if "messages/batches" in url_route and "results" in url_route:
        return AnthropicBatchesConfig
    else:
        return AnthropicConfig

