
def _normalize_api_base(api_base: Optional[str]) -> str:
    return (api_base or REDUCTO_API_BASE).rstrip("/")

