
def get_unpacked_marks(
    obj: object | type,
    *,
    consider_mro: bool = True,
) -> list[Mark]:
    """Obtain the unpacked marks that are stored on an object.

    If obj is a class and consider_mro is true, return marks applied to
    this class and all of its super-classes in MRO order. If consider_mro
    is false, only return marks applied directly to this class.
    """
    if isinstance(obj, type):
        if not consider_mro:
            mark_lists = [obj.__dict__.get("pytestmark", [])]
        else:
            mark_lists = [
                x.__dict__.get("pytestmark", []) for x in reversed(obj.__mro__)
            ]
        mark_list = []
        for item in mark_lists:
            if isinstance(item, list):
                mark_list.extend(item)
            else:
                mark_list.append(item)
    else:
        mark_attribute = getattr(obj, "pytestmark", [])
        if mark_attribute is None:
            warnings.warn(
                "Module defines a `__getattr__` which returns None for "
                "'pytestmark' instead of raising AttributeError. "
                "Make sure `__getattr__` raises AttributeError for "
                "attributes it does not provide. "
                "See https://github.com/pytest-dev/pytest/issues/8265",
                PytestCollectionWarning,
                stacklevel=2,
            )
            mark_list = []
        elif isinstance(mark_attribute, list):
            mark_list = mark_attribute
        else:
            mark_list = [mark_attribute]
    return list(normalize_mark_list(mark_list))

