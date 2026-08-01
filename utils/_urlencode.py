
def _urlencode(query: t.Mapping[str, str] | t.Iterable[tuple[str, str]]) -> str:
    items = [x for x in iter_multi_items(query) if x[1] is not None]
    # safe = https://url.spec.whatwg.org/#percent-encoded-bytes
    return urlencode(items, safe="!$'()*,/:;?@")

