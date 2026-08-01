
def is_from_cache(response: Response) -> bool:
    return getattr(response, "from_cache", False)

