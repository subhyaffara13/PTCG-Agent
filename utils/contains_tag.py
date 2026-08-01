
def contains_tag(tag: str, string: str) -> bool:
    return bool(re.search(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL))

