
def make_attrgetter(
    environment: "Environment",
    attribute: t.Optional[t.Union[str, int]],
    postprocess: t.Optional[t.Callable[[t.Any], t.Any]] = None,
    default: t.Optional[t.Any] = None,
) -> t.Callable[[t.Any], t.Any]:
    """Returns a callable that looks up the given attribute from a
    passed object with the rules of the environment.  Dots are allowed
    to access attributes of attributes.  Integer parts in paths are
    looked up as integers.
    """
    parts = _prepare_attribute_parts(attribute)

    def attrgetter(item: t.Any) -> t.Any:
        for part in parts:
            item = environment.getitem(item, part)

            if default is not None and isinstance(item, Undefined):
                item = default

        if postprocess is not None:
            item = postprocess(item)

        return item

    return attrgetter

