
def ensure_can_construct_http_header_dict(
    potential: object,
) -> ValidHTTPHeaderSource | None:
    if isinstance(potential, HTTPHeaderDict):
        return potential
    elif isinstance(potential, typing.Mapping):
        # Full runtime checking of the contents of a Mapping is expensive, so for the
        # purposes of typechecking, we assume that any Mapping is the right shape.
        return typing.cast(typing.Mapping[str, str], potential)
    elif isinstance(potential, typing.Iterable):
        # Similarly to Mapping, full runtime checking of the contents of an Iterable is
        # expensive, so for the purposes of typechecking, we assume that any Iterable
        # is the right shape.
        return typing.cast(typing.Iterable[tuple[str, str]], potential)
    elif hasattr(potential, "keys") and hasattr(potential, "__getitem__"):
        return typing.cast("HasGettableStringKeys", potential)
    else:
        return None


def ensure_can_construct_http_header_dict(
    potential: object,
) -> ValidHTTPHeaderSource | None:
    if isinstance(potential, HTTPHeaderDict):
        return potential
    elif isinstance(potential, typing.Mapping):
        # Full runtime checking of the contents of a Mapping is expensive, so for the
        # purposes of typechecking, we assume that any Mapping is the right shape.
        return typing.cast(typing.Mapping[str, str], potential)
    elif isinstance(potential, typing.Iterable):
        # Similarly to Mapping, full runtime checking of the contents of an Iterable is
        # expensive, so for the purposes of typechecking, we assume that any Iterable
        # is the right shape.
        return typing.cast(typing.Iterable[tuple[str, str]], potential)
    elif hasattr(potential, "keys") and hasattr(potential, "__getitem__"):
        return typing.cast("HasGettableStringKeys", potential)
    else:
        return None

