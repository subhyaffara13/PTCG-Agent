from typing import Dict

def _append_query_params(url: str, params: Dict[str, str]) -> str:
    parsed = urlparse(url)
    query_params = parse_qsl(parsed.query, keep_blank_values=True)
    query_params.extend(params.items())
    return urlunparse(parsed._replace(query=urlencode(query_params)))

