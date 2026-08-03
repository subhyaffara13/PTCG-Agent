from typing import Any, Dict, List, Optional

def _match_deployment(
    deployment: Any,
    request_tags: Optional[List[str]],
    header_strings: List[str],
    match_any: bool,
) -> Optional[Dict[str, str]]:
    """
    Determine whether *deployment* matches the current request.

    Returns {"matched_via": ..., "matched_value": ...} if the deployment
    should be included, or None if it should be excluded.

    Priority:
      1. Exact tag match (respects match_any semantics).
      2. Regex match — skipped when match_any=False and the tag check already
         ran and failed, so the regex cannot override strict-tag policy.
    """
    litellm_params = deployment.get("litellm_params", {})
    deployment_tags: Optional[List[str]] = litellm_params.get("tags")
    deployment_tag_regex: Optional[List[str]] = litellm_params.get("tag_regex")

    # 1. Exact tag match (existing behaviour).
    if deployment_tags and request_tags:
        if is_valid_deployment_tag(deployment_tags, request_tags, match_any):
            matched_value = next(
                (t for t in deployment_tags if t in set(request_tags)),
                deployment_tags[0],
            )
            return {"matched_via": "tags", "matched_value": matched_value}

    # 2. Regex match against request headers.
    # When match_any=False and the deployment has plain tags, the strict tag
    # check either didn't run (no request tags) or failed (step 1 returned
    # None).  Block the regex path so it cannot circumvent the operator's
    # strict-tag policy.
    deployment_has_plain_tags = deployment_tags is not None and len(deployment_tags) > 0
    strict_tag_check_failed = not match_any and deployment_has_plain_tags
    if deployment_tag_regex and header_strings and not strict_tag_check_failed:
        regex_match = _is_valid_deployment_tag_regex(
            deployment_tag_regex, header_strings
        )
        if regex_match is not None:
            return {"matched_via": "tag_regex", "matched_value": regex_match}

    return None

