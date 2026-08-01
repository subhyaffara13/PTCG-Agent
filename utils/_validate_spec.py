
def _validate_spec(spec: object, /) -> TypeGuard[tuple[str, str]]:
    return (
        isinstance(spec, tuple)
        and len(spec) == 2
        and isinstance(spec[0], str)
        and isinstance(spec[1], str)
    )


def _validate_spec(spec: object, /) -> TypeGuard[tuple[str, str]]:
    return (
        isinstance(spec, tuple)
        and len(spec) == 2
        and isinstance(spec[0], str)
        and isinstance(spec[1], str)
    )

