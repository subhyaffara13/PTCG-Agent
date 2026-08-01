
def normalize_subpath(subpath: AnyStr | None, encode: bool | None = True) -> str | None:
    if not subpath:
        return None

    subpath_str = subpath if isinstance(subpath, str) else subpath.decode("utf-8")
    quoter = get_quoter(encode)
    segments = subpath_str.split("/")
    segments = [quoter(s) for s in segments if s.strip() and s not in (".", "..")]
    subpath_str = "/".join(segments)
    return subpath_str or None

