import os
from typing import List, Optional

def get_datadog_tags(
    standard_logging_object: Optional[StandardLoggingPayload] = None,
) -> List[str]:
    """Build Datadog tags as a list of individual tag strings.

    Returns a list of "key:value" strings suitable for Datadog LLM Observability
    (which expects tags as an array). For Datadog Logs API (ddtags), join with
    comma: ",".join(get_datadog_tags(...)).
    """

    base_tags = {
        "env": get_datadog_env(),
        "service": get_datadog_service(),
        "version": os.getenv("DD_VERSION", "unknown"),
        "HOSTNAME": get_datadog_hostname(),
        "POD_NAME": get_datadog_pod_name(),
    }

    tags: List[str] = [f"{k}:{v}" for k, v in base_tags.items()]

    if standard_logging_object:
        request_tags = standard_logging_object.get("request_tags", []) or []
        tags.extend(f"request_tag:{tag}" for tag in request_tags)

        # Add Team Tag
        metadata = standard_logging_object.get("metadata", {}) or {}
        team_tag = (
            metadata.get("user_api_key_team_alias")
            or metadata.get("team_alias")
            or metadata.get("user_api_key_team_id")
            or metadata.get("team_id")
        )
        if team_tag:
            tags.append(f"team:{team_tag}")

    return tags

