
def _relaxedSetattr(object: Any, attr: str, value: Any) -> None:
    try:
        setattr(object, attr, value)
    except AttributeError:
        pass

