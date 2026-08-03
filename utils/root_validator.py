from typing import Any, Callable, Optional, Union

def root_validator(
    *,
    # if you don't specify `pre` the default is `pre=False`
    # which means you need to specify `skip_on_failure=True`
    skip_on_failure: Literal[True],
    allow_reuse: bool = ...,
) -> Callable[
    [_V1RootValidatorFunctionType],
    _V1RootValidatorFunctionType,
]: ...


def root_validator(
    *,
    # if you specify `pre=True` then you don't need to specify
    # `skip_on_failure`, in fact it is not allowed as an argument!
    pre: Literal[True],
    allow_reuse: bool = ...,
) -> Callable[
    [_V1RootValidatorFunctionType],
    _V1RootValidatorFunctionType,
]: ...


def root_validator(
    *,
    # if you explicitly specify `pre=False` then you
    # MUST specify `skip_on_failure=True`
    pre: Literal[False],
    skip_on_failure: Literal[True],
    allow_reuse: bool = ...,
) -> Callable[
    [_V1RootValidatorFunctionType],
    _V1RootValidatorFunctionType,
]: ...


def root_validator(
    *__args,
    pre: bool = False,
    skip_on_failure: bool = False,
    allow_reuse: bool = False,
) -> Any:
    """Decorate methods on a model indicating that they should be used to validate (and perhaps
    modify) data either before or after standard model parsing/validation is performed.

    Args:
        pre (bool, optional): Whether this validator should be called before the standard
            validators (else after). Defaults to False.
        skip_on_failure (bool, optional): Whether to stop validation and return as soon as a
            failure is encountered. Defaults to False.
        allow_reuse (bool, optional): Whether to track and raise an error if another validator
            refers to the decorated function. Defaults to False.

    Returns:
        Any: A decorator that can be used to decorate a function to be used as a root_validator.
    """
    warn(
        'Pydantic V1 style `@root_validator` validators are deprecated.'
        ' You should migrate to Pydantic V2 style `@model_validator` validators,'
        ' see the migration guide for more details',
        DeprecationWarning,
        stacklevel=2,
    )

    if __args:
        # Ensure a nice error is raised if someone attempts to use the bare decorator
        return root_validator()(*__args)  # type: ignore

    if allow_reuse is True:  # pragma: no cover
        warn(_ALLOW_REUSE_WARNING_MESSAGE, DeprecationWarning, stacklevel=2)
    mode: Literal['before', 'after'] = 'before' if pre is True else 'after'
    if pre is False and skip_on_failure is not True:
        raise PydanticUserError(
            'If you use `@root_validator` with pre=False (the default) you MUST specify `skip_on_failure=True`.'
            ' Note that `@root_validator` is deprecated and should be replaced with `@model_validator`.',
            code='root-validator-pre-skip',
        )

    wrap = partial(_decorators_v1.make_v1_generic_root_validator, pre=pre)

    def dec(f: Callable[..., Any] | classmethod[Any, Any, Any] | staticmethod[Any, Any]) -> Any:
        if _decorators.is_instance_method_from_sig(f):
            raise TypeError('`@root_validator` cannot be applied to instance methods')
        # auto apply the @classmethod decorator
        res = _decorators.ensure_classmethod_based_on_signature(f)
        dec_info = _decorators.RootValidatorDecoratorInfo(mode=mode)
        return _decorators.PydanticDescriptorProxy(res, dec_info, shim=wrap)

    return dec


def root_validator(_func: AnyCallable) -> 'AnyClassMethod':
    ...


def root_validator(
    *, pre: bool = False, allow_reuse: bool = False, skip_on_failure: bool = False
) -> Callable[[AnyCallable], 'AnyClassMethod']:
    ...


def root_validator(
    _func: Optional[AnyCallable] = None, *, pre: bool = False, allow_reuse: bool = False, skip_on_failure: bool = False
) -> Union['AnyClassMethod', Callable[[AnyCallable], 'AnyClassMethod']]:
    """
    Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
    before or after standard model parsing/validation is performed.
    """
    if _func:
        f_cls = _prepare_validator(_func, allow_reuse)
        setattr(
            f_cls, ROOT_VALIDATOR_CONFIG_KEY, Validator(func=f_cls.__func__, pre=pre, skip_on_failure=skip_on_failure)
        )
        return f_cls

    def dec(f: AnyCallable) -> 'AnyClassMethod':
        f_cls = _prepare_validator(f, allow_reuse)
        setattr(
            f_cls, ROOT_VALIDATOR_CONFIG_KEY, Validator(func=f_cls.__func__, pre=pre, skip_on_failure=skip_on_failure)
        )
        return f_cls

    return dec

