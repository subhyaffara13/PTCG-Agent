
def normalize_namespace(
    namespace: AnyStr | None, ptype: str | None, encode: bool | None = True
) -> str | None:
    if not namespace:
        return None

    namespace_str = namespace if isinstance(namespace, str) else namespace.decode("utf-8")
    namespace_str = namespace_str.strip().strip("/")
    if ptype in (
        "bitbucket",
        "github",
        "pypi",
        "gitlab",
        "composer",
        "luarocks",
        "qpkg",
        "alpm",
        "apk",
        "hex",
    ):
        namespace_str = namespace_str.lower()
    if ptype and ptype in ("cpan"):
        namespace_str = namespace_str.upper()
    segments = [seg for seg in namespace_str.split("/") if seg.strip()]
    segments_quoted = map(get_quoter(encode), segments)
    return "/".join(segments_quoted) or None

