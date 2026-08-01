
def set_default_hash_func(cls: type[BaseModel], bases: tuple[type[Any], ...]) -> None:
    base_hash_func = get_attribute_from_bases(bases, '__hash__')
    new_hash_func = make_hash_func(cls)
    if base_hash_func in {None, object.__hash__} or getattr(base_hash_func, '__code__', None) == new_hash_func.__code__:
        # If `__hash__` is some default, we generate a hash function.
        # It will be `None` if not overridden from BaseModel.
        # It may be `object.__hash__` if there is another
        # parent class earlier in the bases which doesn't override `__hash__` (e.g. `typing.Generic`).
        # It may be a value set by `set_default_hash_func` if `cls` is a subclass of another frozen model.
        # In the last case we still need a new hash function to account for new `model_fields`.
        cls.__hash__ = new_hash_func

