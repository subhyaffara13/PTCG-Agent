from typing import Dict, Optional

def pop_bedrock_invoke_output_config_format(request_body: Dict) -> Optional[Dict]:
    """
    Remove and return Anthropic's nested ``output_config.format`` field.

    Bedrock Invoke paths convert the schema to inline message text. Any remaining
    ``output_config`` keys, such as ``effort``, are left in place.
    """
    output_config = request_body.get("output_config")
    if not isinstance(output_config, dict):
        return None

    output_format = output_config.pop("format", None)
    if not output_config:
        request_body.pop("output_config", None)

    if isinstance(output_format, dict):
        return output_format
    return None

