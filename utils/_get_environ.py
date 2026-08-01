
def _get_environ(obj: WSGIEnvironment | Request) -> WSGIEnvironment:
    env = getattr(obj, "environ", obj)
    assert isinstance(env, dict), (
        f"{type(obj).__name__!r} is not a WSGI environment (has to be a dict)"
    )
    return env

