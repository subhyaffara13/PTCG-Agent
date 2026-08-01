
def validator(
    __field: str,
    *fields: str,
    pre: bool = False,
    each_item: bool = False,
    always: bool = False,
    check_fields: bool | None = None,
    allow_reuse: bool = False,
) -> Callable[[_V1ValidatorType], _V1ValidatorType]:
    """Decorate methods on the class indicating that they should be used to validate fields.

    Args:
        __field (str): The first field the validator should be called on; this is separate
            from `fields` to ensure an error is raised if you don't pass at least one.
        *fields (str): Additional field(s) the validator should be called on.
        pre (bool, optional): Whether this validator should be called before the standard
            validators (else after). Defaults to False.
        each_item (bool, optional): For complex objects (sets, lists etc.) whether to validate
            individual elements rather than the whole object. Defaults to False.
        always (bool, optional): Whether this method and other validators should be called even if
            the value is missing. Defaults to False.
        check_fields (bool | None, optional): Whether to check that the fields actually exist on the model.
            Defaults to None.
        allow_reuse (bool, optional): Whether to track and raise an error if another validator refers to
            the decorated function. Defaults to False.

    Returns:
        Callable: A decorator that can be used to decorate a
            function to be used as a validator.
    """
    warn(
        'Pydantic V1 style `@validator` validators are deprecated.'
        ' You should migrate to Pydantic V2 style `@field_validator` validators,'
        ' see the migration guide for more details',
        DeprecationWarning,
        stacklevel=2,
    )

    if allow_reuse is True:  # pragma: no cover
        warn(_ALLOW_REUSE_WARNING_MESSAGE, DeprecationWarning, stacklevel=2)
    fields = __field, *fields
    if isinstance(fields[0], FunctionType):
        raise PydanticUserError(
            '`@validator` should be used with fields and keyword arguments, not bare. '
            "E.g. usage should be `@validator('<field_name>', ...)`",
            code='decorator-missing-arguments',
        )
    elif not all(isinstance(field, str) for field in fields):
        raise PydanticUserError(
            '`@validator` fields should be passed as separate string args. '
            "E.g. usage should be `@validator('<field_name_1>', '<field_name_2>', ...)`",
            code='decorator-invalid-fields',
        )

    mode: Literal['before', 'after'] = 'before' if pre is True else 'after'

    def dec(f: Any) -> _decorators.PydanticDescriptorProxy[Any]:
        if _decorators.is_instance_method_from_sig(f):
            raise PydanticUserError(
                '`@validator` cannot be applied to instance methods', code='validator-instance-method'
            )
        # auto apply the @classmethod decorator
        f = _decorators.ensure_classmethod_based_on_signature(f)
        wrap = _decorators_v1.make_generic_v1_field_validator
        validator_wrapper_info = _decorators.ValidatorDecoratorInfo(
            fields=fields,
            mode=mode,
            each_item=each_item,
            always=always,
            check_fields=check_fields,
        )
        return _decorators.PydanticDescriptorProxy(f, validator_wrapper_info, shim=wrap)

    return dec  # type: ignore[return-value]


def validator(
    *fields: str,
    pre: bool = False,
    each_item: bool = False,
    always: bool = False,
    check_fields: bool = True,
    whole: Optional[bool] = None,
    allow_reuse: bool = False,
) -> Callable[[AnyCallable], 'AnyClassMethod']:
    """
    Decorate methods on the class indicating that they should be used to validate fields
    :param fields: which field(s) the method should be called on
    :param pre: whether or not this validator should be called before the standard validators (else after)
    :param each_item: for complex objects (sets, lists etc.) whether to validate individual elements rather than the
      whole object
    :param always: whether this method and other validators should be called even if the value is missing
    :param check_fields: whether to check that the fields actually exist on the model
    :param allow_reuse: whether to track and raise an error if another validator refers to the decorated function
    """
    if not fields:
        raise ConfigError('validator with no fields specified')
    elif isinstance(fields[0], FunctionType):
        raise ConfigError(
            "validators should be used with fields and keyword arguments, not bare. "  # noqa: Q000
            "E.g. usage should be `@validator('<field_name>', ...)`"
        )
    elif not all(isinstance(field, str) for field in fields):
        raise ConfigError(
            "validator fields should be passed as separate string args. "  # noqa: Q000
            "E.g. usage should be `@validator('<field_name_1>', '<field_name_2>', ...)`"
        )

    if whole is not None:
        warnings.warn(
            'The "whole" keyword argument is deprecated, use "each_item" (inverse meaning, default False) instead',
            DeprecationWarning,
        )
        assert each_item is False, '"each_item" and "whole" conflict, remove "whole"'
        each_item = not whole

    def dec(f: AnyCallable) -> 'AnyClassMethod':
        f_cls = _prepare_validator(f, allow_reuse)
        setattr(
            f_cls,
            VALIDATOR_CONFIG_KEY,
            (
                fields,
                Validator(func=f_cls.__func__, pre=pre, each_item=each_item, always=always, check_fields=check_fields),
            ),
        )
        return f_cls

    return dec


def validator(flag_name, message='Flag validation failed',
              flag_values=_flagvalues.FLAGS):
  """A function decorator for defining a flag validator.

  Registers the decorated function as a validator for flag_name, e.g.::

      @flags.validator('foo')
      def _CheckFoo(foo):
        ...

  See :func:`register_validator` for the specification of checker function.

  Args:
    flag_name: str | FlagHolder, name or holder of the flag to be checked.
        Positional-only parameter.
    message: str, error text to be shown to the user if checker returns False.
        If checker raises flags.ValidationError, message from the raised
        error will be shown.
    flag_values: flags.FlagValues, optional FlagValues instance to validate
        against.
  Returns:
    A function decorator that registers its function argument as a validator.
  Raises:
    AttributeError: Raised when flag_name is not registered as a valid flag
        name.
  """

  def decorate(function):
    register_validator(flag_name, function,
                       message=message,
                       flag_values=flag_values)
    return function
  return decorate

