
def map_generic_model_arguments(cls: type[BaseModel], args: tuple[Any, ...]) -> dict[TypeVar, Any]:
    """Return a mapping between the parameters of a generic model and the provided arguments during parameterization.

    Raises:
        TypeError: If the number of arguments does not match the parameters (i.e. if providing too few or too many arguments).

    Example:
        ```python {test="skip" lint="skip"}
        class Model[T, U, V = int](BaseModel): ...

        map_generic_model_arguments(Model, (str, bytes))
        #> {T: str, U: bytes, V: int}

        map_generic_model_arguments(Model, (str,))
        #> TypeError: Too few arguments for <class '__main__.Model'>; actual 1, expected at least 2

        map_generic_model_arguments(Model, (str, bytes, int, complex))
        #> TypeError: Too many arguments for <class '__main__.Model'>; actual 4, expected 3
        ```

    Note:
        This function is analogous to the private `typing._check_generic_specialization` function.
    """
    parameters = cls.__pydantic_generic_metadata__['parameters']
    expected_len = len(parameters)
    typevars_map: dict[TypeVar, Any] = {}

    _missing = object()
    for parameter, argument in zip_longest(parameters, args, fillvalue=_missing):
        if parameter is _missing:
            raise TypeError(f'Too many arguments for {cls}; actual {len(args)}, expected {expected_len}')

        if argument is _missing:
            param = cast(TypeVar, parameter)
            try:
                has_default = param.has_default()  # pyright: ignore[reportAttributeAccessIssue]
            except AttributeError:
                # Happens if using `typing.TypeVar` (and not `typing_extensions`) on Python < 3.13.
                has_default = False
            if has_default:
                # The default might refer to other type parameters. For an example, see:
                # https://typing.python.org/en/latest/spec/generics.html#type-parameters-as-parameters-to-generics
                typevars_map[param] = replace_types(param.__default__, typevars_map)  # pyright: ignore[reportAttributeAccessIssue]
            else:
                expected_len -= sum(hasattr(p, 'has_default') and p.has_default() for p in parameters)  # pyright: ignore[reportAttributeAccessIssue]
                raise TypeError(f'Too few arguments for {cls}; actual {len(args)}, expected at least {expected_len}')
        else:
            param = cast(TypeVar, parameter)
            typevars_map[param] = argument

    return typevars_map

