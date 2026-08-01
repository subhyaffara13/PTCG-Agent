
def _assign(attr_name: str, value: str, has_on_setattr: bool) -> str:
    """
    Unless *attr_name* has an on_setattr hook, use normal assignment. Otherwise
    relegate to _setattr.
    """
    if has_on_setattr:
        return _setattr(attr_name, value, True)

    return f"self.{attr_name} = {value}"

