
def _anthropic_messages_optional_param_keys() -> FrozenSet[str]:
    """
    Valid AnthropicMessagesRequestOptionalParams keys.

    ``typing.get_type_hints`` is ~80us/call and this TypedDict is static, so
    resolving it once per process instead of once per request removes a fixed
    full-pass cost from the /v1/messages request-parse path.
    """
    return frozenset(get_type_hints(AnthropicMessagesRequestOptionalParams).keys())

