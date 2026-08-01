
def callable_with_ellipsis(any_type: AnyType, ret_type: Type, fallback: Instance) -> CallableType:
    """Construct type Callable[..., ret_type]."""
    return CallableType(
        [any_type, any_type],
        [ARG_STAR, ARG_STAR2],
        [None, None],
        ret_type=ret_type,
        fallback=fallback,
        is_ellipsis_args=True,
    )

