
def _transfer_attrs(fr: object, to: object) -> None:
    for attr_name in dir(fr):
        attr_val = getattr(fr, attr_name)
        if (
            not callable(attr_val)
            and not attr_name.startswith("__")
            and not hasattr(to, attr_name)
        ):
            setattr(to, attr_name, attr_val)

