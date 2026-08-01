
def _quote_path(value: str) -> str:
    if YARL_VERSION < (1, 6):
        value = value.replace("%", "%25")
    return URL.build(path=value, encoded=False).raw_path

