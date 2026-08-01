
def isproperty(o: object, attr: str) -> bool:
    return isinstance(getattr(type(o), attr, None), property)

