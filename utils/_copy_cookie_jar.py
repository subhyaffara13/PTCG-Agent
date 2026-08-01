
def _copy_cookie_jar(jar: CookieJar | None) -> CookieJar | None:  # type: ignore[reportUnusedFunction]  # cross-module usage in models.py
    if jar is None:
        return None

    if copy_method := getattr(jar, "copy", None):
        # We're dealing with an instance of RequestsCookieJar
        return copy_method()
    # We're dealing with a generic CookieJar instance
    new_jar = copy.copy(jar)
    new_jar.clear()
    for cookie in jar:
        new_jar.set_cookie(copy.copy(cookie))
    return new_jar


def _copy_cookie_jar(jar):
    if jar is None:
        return None

    if hasattr(jar, "copy"):
        # We're dealing with an instance of RequestsCookieJar
        return jar.copy()
    # We're dealing with a generic CookieJar instance
    new_jar = copy.copy(jar)
    new_jar.clear()
    for cookie in jar:
        new_jar.set_cookie(copy.copy(cookie))
    return new_jar

