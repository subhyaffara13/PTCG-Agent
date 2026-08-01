
def get_range(session, url, start, end, **kwargs):
    # explicit get a range when we know it must be safe
    kwargs = kwargs.copy()
    headers = kwargs.pop("headers", {}).copy()
    headers["Range"] = f"bytes={start}-{end - 1}"
    r = session.get(url, headers=headers, **kwargs)
    r.raise_for_status()
    return r.content

