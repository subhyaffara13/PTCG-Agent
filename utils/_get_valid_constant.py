
def _get_valid_constant(attr, v, owner_type):
    if isinstance(v, _constant_types):
        return v
    elif isinstance(v, (tuple, list)):
        return tuple(_get_valid_constant(attr, x, owner_type) for x in v)
    constants = ", ".join(torch.typename(typ) for typ in _constant_types)
    raise TypeError(
        textwrap.dedent(
            f"""
        '{torch.typename(type(v))}' object in attribute '{owner_type}.{attr}' is not a valid constant.
        Valid constants are:
        1. a nn.ModuleList
        2. a value of type {{{constants}}}
        3. a list or tuple of (2)
        """
        )
    )

