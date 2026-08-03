from typing import Any, Dict, Union

def build_cli_sso_attribution_metadata(
    result: Union[CustomOpenID, OpenID, dict],
) -> Dict[str, Any]:
    """
    Build allowlisted, non-secret scalar attribution metadata from an SSO result.

    Sources are configured via CLI_SSO_CLAIM_MAP / LITELLM_CLI_SSO_CLAIM_MAP and
    may include claims captured by GENERIC_USER_EXTRA_ATTRIBUTES on CustomOpenID.
    """
    claim_map = _parse_cli_sso_claim_map()
    if not claim_map:
        return {}

    metadata: Dict[str, Any] = {}
    for source_claim, dest_key in claim_map:
        if not _is_safe_cli_sso_metadata_dest_key(dest_key):
            verbose_proxy_logger.debug(
                f"Skipping unsafe CLI SSO metadata destination key: {dest_key}"
            )
            continue

        raw_value = _extract_sso_claim_value(result=result, claim_path=source_claim)
        if not _is_safe_cli_sso_scalar_claim_value(raw_value):
            continue

        _set_nested_metadata_value(
            metadata=metadata, key_path=dest_key, value=raw_value
        )

    return metadata

