
def validate_arguments(
    func: None = None, *, config: 'ConfigType' = None
) -> Callable[['AnyCallableT'], 'AnyCallableT']: ...


def validate_arguments(func: 'AnyCallableT') -> 'AnyCallableT': ...


def validate_arguments(func: Optional['AnyCallableT'] = None, *, config: 'ConfigType' = None) -> Any:
    """Decorator to validate the arguments passed to a function."""
    warnings.warn(
        'The `validate_arguments` method is deprecated; use `validate_call` instead.',
        PydanticDeprecatedSince20,
        stacklevel=2,
    )

    def validate(_func: 'AnyCallable') -> 'AnyCallable':
        vd = ValidatedFunction(_func, config)

        @wraps(_func)
        def wrapper_function(*args: Any, **kwargs: Any) -> Any:
            return vd.call(*args, **kwargs)

        wrapper_function.vd = vd  # type: ignore
        wrapper_function.validate = vd.init_model_instance  # type: ignore
        wrapper_function.raw_function = vd.raw_function  # type: ignore
        wrapper_function.model = vd.model  # type: ignore
        return wrapper_function

    if func:
        return validate(func)
    else:
        return validate


def validate_arguments(func: None = None, *, config: 'ConfigType' = None) -> Callable[['AnyCallableT'], 'AnyCallableT']:
    ...


def validate_arguments(func: 'AnyCallableT') -> 'AnyCallableT':
    ...


def validate_arguments(func: Optional['AnyCallableT'] = None, *, config: 'ConfigType' = None) -> Any:
    """
    Decorator to validate the arguments passed to a function.
    """

    def validate(_func: 'AnyCallable') -> 'AnyCallable':
        vd = ValidatedFunction(_func, config)

        @wraps(_func)
        def wrapper_function(*args: Any, **kwargs: Any) -> Any:
            return vd.call(*args, **kwargs)

        wrapper_function.vd = vd  # type: ignore
        wrapper_function.validate = vd.init_model_instance  # type: ignore
        wrapper_function.raw_function = vd.raw_function  # type: ignore
        wrapper_function.model = vd.model  # type: ignore
        return wrapper_function

    if func:
        return validate(func)
    else:
        return validate

