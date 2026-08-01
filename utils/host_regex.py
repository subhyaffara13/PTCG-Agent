
def host_regex() -> Pattern[str]:
    global _host_regex_cache
    if _host_regex_cache is None:
        _host_regex_cache = re.compile(
            _host_regex,
            re.IGNORECASE,
        )
    return _host_regex_cache

