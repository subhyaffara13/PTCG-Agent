
def yield_everything(obj):
    """Yield every item in a container as bytes

    Allows any JSONable object to be passed to an HMAC digester
    without having to serialize the whole thing.
    """
    if isinstance(obj, dict):
        for key in sorted(obj):
            value = obj[key]
            assert isinstance(key, str)
            yield key.encode()
            yield from yield_everything(value)
    elif isinstance(obj, (list, tuple)):
        for element in obj:
            yield from yield_everything(element)
    elif isinstance(obj, str):
        yield obj.encode("utf8")
    else:
        yield str(obj).encode("utf8")

