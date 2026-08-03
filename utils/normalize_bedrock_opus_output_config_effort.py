from typing import Any

def normalize_bedrock_opus_output_config_effort(model: str, output_config: Any) -> None:
    """
    Normalize Anthropic ``output_config.effort`` values for Bedrock Opus ids.

    Bedrock's Claude Opus request validator can accept a narrower effort
    vocabulary than Anthropic's compatibility surface. The Bedrock ceiling is
    read from ``model_prices_and_context_window.json`` via
    ``bedrock_output_config_effort_ceiling``.

    Mutates ``output_config`` in place so callers can accept Claude Code's
    ``xhigh`` input without forwarding a provider-invalid value.
    """
    if not isinstance(output_config, dict):
        return

    effort = output_config.get("effort")
    if effort not in _BEDROCK_OUTPUT_CONFIG_EFFORT_ORDER:
        return

    ceiling = _get_bedrock_output_config_effort_ceiling(model)
    if ceiling is None:
        return

    if (
        _BEDROCK_OUTPUT_CONFIG_EFFORT_ORDER[effort]
        > _BEDROCK_OUTPUT_CONFIG_EFFORT_ORDER[ceiling]
    ):
        output_config["effort"] = ceiling

