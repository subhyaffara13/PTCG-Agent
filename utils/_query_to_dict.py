
def _query_to_dict(query: str) -> dict[str, str]:
    return {
        pair[0]: pair[1]
        for pair in (pair.split("=") for pair in filter(None, query.split("&")))
    }

