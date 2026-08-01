
def _get_timeout(params: RendezvousParameters, key: str) -> timedelta | None:
    timeout = params.get_as_int(key + "_timeout")
    if timeout is None:
        return None
    return timedelta(seconds=timeout)

