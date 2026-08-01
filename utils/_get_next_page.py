
def _get_next_page(response: httpx.Response) -> str | None:
    return response.links.get("next", {}).get("url")

