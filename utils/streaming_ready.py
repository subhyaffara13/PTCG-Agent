
def streaming_ready() -> bool | None:
    if _fetcher:
        return _fetcher.streaming_ready
    else:
        return None  # no fetcher, return None to signify that


def streaming_ready() -> bool | None:
    if _fetcher:
        return _fetcher.streaming_ready
    else:
        return None  # no fetcher, return None to signify that

