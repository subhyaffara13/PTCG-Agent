
def is_type(type_hint, comp_type) -> bool:  # type: ignore[no-untyped-def]
    """
    Determines if type_hint is comp_type. There are some type annotations that this doesn't work for.
    I think it's because some Type annotations are Type Objects and some are Special Forms, but not sure.
    There's definite room for improvement to make this more general for someone who deeply understands
    Python types.
    """
    return type_hint is comp_type or get_origin(type_hint) is comp_type


def is_type(any_msg: Any, des: descriptor.Descriptor) -> bool:
  return any_msg.Is(des)

