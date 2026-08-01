
def _sso_result_to_dict(result: Union[CustomOpenID, OpenID, dict]) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    if hasattr(result, "model_dump"):
        dumped = result.model_dump()
        if isinstance(dumped, dict):
            return cast(Dict[str, Any], dumped)
    return {}

