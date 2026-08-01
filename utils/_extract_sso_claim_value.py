
def _extract_sso_claim_value(
    result: Union[CustomOpenID, OpenID, dict], claim_path: str
) -> Any:
    extra_fields = getattr(result, "extra_fields", None)
    if isinstance(extra_fields, dict):
        if claim_path in extra_fields:
            return extra_fields[claim_path]
        nested = _get_nested_claim_value(extra_fields, claim_path)
        if nested is not None:
            return nested

    if isinstance(result, dict):
        return _get_nested_claim_value(result, claim_path)

    result_dict = _sso_result_to_dict(result)
    return _get_nested_claim_value(result_dict, claim_path)

