import re

def multi_host_url_regex() -> Pattern[str]:
    """
    Compiled multi host url regex.

    Additionally to `url_regex` it allows to match multiple hosts.
    E.g. host1.db.net,host2.db.net
    """
    global _multi_host_url_regex_cache
    if _multi_host_url_regex_cache is None:
        _multi_host_url_regex_cache = re.compile(
            rf'{_scheme_regex}{_user_info_regex}'
            r'(?P<hosts>([^/]*))'  # validation occurs later
            rf'{_path_regex}{_query_regex}{_fragment_regex}',
            re.IGNORECASE,
        )
    return _multi_host_url_regex_cache

