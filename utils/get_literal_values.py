from typing import Any

def get_literal_values(
    annotation: Any,
    /,
    *,
    type_check: bool = False,
    unpack_type_aliases: Literal['skip', 'lenient', 'eager'] = 'eager',
) -> Generator[Any]:
    """Yield the values contained in the provided [`Literal`][typing.Literal] [special form][].

    Args:
        annotation: The [`Literal`][typing.Literal] [special form][] to unpack.
        type_check: Whether to check if the literal values are [legal parameters][literal-legal-parameters].
            Raises a [`TypeError`][] otherwise.
        unpack_type_aliases: What to do when encountering [PEP 695](https://peps.python.org/pep-0695/)
            [type aliases][type-aliases]. Can be one of:

            - `'skip'`: Do not try to parse type aliases. Note that this can lead to incorrect results:
              ```pycon
              >>> type MyAlias = Literal[1, 2]
              >>> list(get_literal_values(Literal[MyAlias, 3], unpack_type_aliases="skip"))
              [MyAlias, 3]
              ```

            - `'lenient'`: Try to parse type aliases, and fallback to `'skip'` if the type alias can't be inspected
              (because of an undefined forward reference).

            - `'eager'`: Parse type aliases and raise any encountered [`NameError`][] exceptions (the default):
              ```pycon
              >>> type MyAlias = Literal[1, 2]
              >>> list(get_literal_values(Literal[MyAlias, 3], unpack_type_aliases="eager"))
              [1, 2, 3]
              ```

    Note:
        While `None` is [equivalent to][none] `type(None)`, the runtime implementation of [`Literal`][typing.Literal]
        does not de-duplicate them. This function makes sure this de-duplication is applied:

        ```pycon
        >>> list(get_literal_values(Literal[NoneType, None]))
        [None]
        ```

    Example:
        ```pycon
        >>> type Ints = Literal[1, 2]
        >>> list(get_literal_values(Literal[1, Ints], unpack_type_alias="skip"))
        ["a", Ints]
        >>> list(get_literal_values(Literal[1, Ints]))
        [1, 2]
        >>> list(get_literal_values(Literal[1.0], type_check=True))
        Traceback (most recent call last):
        ...
        TypeError: 1.0 is not a valid literal value, must be one of: int, bytes, str, Enum, None.
        ```
    """
    # `literal` is guaranteed to be a `Literal[...]` special form, so use
    # `__args__` directly instead of calling `get_args()`.

    if unpack_type_aliases == 'skip':
        _has_none = False
        # `Literal` parameters are already deduplicated, no need to do it ourselves.
        # (we only check for `None` and `NoneType`, which should be considered as duplicates).
        for arg in annotation.__args__:
            if type_check:
                _literal_type_check(arg)
            if arg is None or arg is typing_objects.NoneType:
                if not _has_none:
                    yield None
                _has_none = True
            else:
                yield arg
    else:
        # We'll need to manually deduplicate parameters, see the `Literal` implementation in `typing`.
        values_and_type: list[tuple[Any, type[Any]]] = []

        for arg in annotation.__args__:
            # Note: we could also check for generic aliases with a type alias as an origin.
            # However, it is very unlikely that this happens as type variables can't appear in
            # `Literal` forms, so the only valid (but unnecessary) use case would be something like:
            # `type Test[T] = Literal['a']` (and then use `Test[SomeType]`).
            if typing_objects.is_typealiastype(arg):
                try:
                    alias_value = arg.__value__
                except NameError:
                    if unpack_type_aliases == 'eager':
                        raise
                    # unpack_type_aliases == "lenient":
                    if type_check:
                        _literal_type_check(arg)
                    values_and_type.append((arg, type(arg)))
                else:
                    sub_args = get_literal_values(
                        alias_value, type_check=type_check, unpack_type_aliases=unpack_type_aliases
                    )
                    values_and_type.extend((a, type(a)) for a in sub_args)  # pyright: ignore[reportUnknownArgumentType]
            else:
                if type_check:
                    _literal_type_check(arg)
                if arg is typing_objects.NoneType:
                    values_and_type.append((None, typing_objects.NoneType))
                else:
                    values_and_type.append((arg, type(arg)))  # pyright: ignore[reportUnknownArgumentType]

        try:
            dct = dict.fromkeys(values_and_type)
        except TypeError:
            # Unhashable parameters, the Python implementation allows them
            yield from (p for p, _ in values_and_type)
        else:
            yield from (p for p, _ in dct)

