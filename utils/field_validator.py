
def field_validator(
    field: str,
    /,
    *fields: str,
    mode: Literal['wrap'],
    check_fields: bool | None = ...,
    json_schema_input_type: Any = ...,
) -> Callable[[_V2WrapValidatorType], _V2WrapValidatorType]: ...


def field_validator(
    field: str,
    /,
    *fields: str,
    mode: Literal['before', 'plain'],
    check_fields: bool | None = ...,
    json_schema_input_type: Any = ...,
) -> Callable[[_V2BeforeAfterOrPlainValidatorType], _V2BeforeAfterOrPlainValidatorType]: ...


def field_validator(
    field: str,
    /,
    *fields: str,
    mode: Literal['after'] = ...,
    check_fields: bool | None = ...,
) -> Callable[[_V2BeforeAfterOrPlainValidatorType], _V2BeforeAfterOrPlainValidatorType]: ...


def field_validator(  # noqa: D417
    field: str,
    /,
    *fields: str,
    mode: FieldValidatorModes = 'after',
    check_fields: bool | None = None,
    json_schema_input_type: Any = PydanticUndefined,
) -> Callable[[Any], Any]:
    """!!! abstract "Usage Documentation"
        [field validators](../concepts/validators.md#field-validators)

    Decorate methods on the class indicating that they should be used to validate fields.

    Example usage:
    ```python
    from typing import Any

    from pydantic import (
        BaseModel,
        ValidationError,
        field_validator,
    )

    class Model(BaseModel):
        a: str

        @field_validator('a')
        @classmethod
        def ensure_foobar(cls, v: Any):
            if 'foobar' not in v:
                raise ValueError('"foobar" not found in a')
            return v

    print(repr(Model(a='this is foobar good')))
    #> Model(a='this is foobar good')

    try:
        Model(a='snap')
    except ValidationError as exc_info:
        print(exc_info)
        '''
        1 validation error for Model
        a
          Value error, "foobar" not found in a [type=value_error, input_value='snap', input_type=str]
        '''
    ```

    For more in depth examples, see [Field Validators](../concepts/validators.md#field-validators).

    Args:
        *fields: The field names the validator should apply to.
        mode: Specifies whether to validate the fields before or after validation.
        check_fields: Whether to check that the fields actually exist on the model.
        json_schema_input_type: The input type of the function. This is only used to generate
            the appropriate JSON Schema (in validation mode) and can only specified
            when `mode` is either `'before'`, `'plain'` or `'wrap'`.

    Raises:
        PydanticUserError:
            - If the decorator is used without any arguments (at least one field name must be provided).
            - If the provided field names are not strings.
            - If `json_schema_input_type` is provided with an unsupported `mode`.
            - If the decorator is applied to an instance method.
    """
    if callable(field) or isinstance(field, classmethod):
        raise PydanticUserError(
            'The `@field_validator` decorator cannot be used without arguments, at least one field must be provided. '
            "For example: `@field_validator('<field_name>', ...)`.",
            code='decorator-missing-arguments',
        )

    if mode not in ('before', 'plain', 'wrap') and json_schema_input_type is not PydanticUndefined:
        raise PydanticUserError(
            f"`json_schema_input_type` can't be used when mode is set to {mode!r}",
            code='validator-input-type',
        )

    if json_schema_input_type is PydanticUndefined and mode == 'plain':
        json_schema_input_type = Any

    fields = field, *fields
    if not all(isinstance(field, str) for field in fields):
        raise PydanticUserError(
            'The provided field names to the `@field_validator` decorator should be strings. '
            "For example: `@field_validator('<field_name_1>', '<field_name_2>', ...).`",
            code='decorator-invalid-fields',
        )

    def dec(
        f: Callable[..., Any] | staticmethod[Any, Any] | classmethod[Any, Any, Any],
    ) -> _decorators.PydanticDescriptorProxy[Any]:
        if _decorators.is_instance_method_from_sig(f):
            raise PydanticUserError(
                'The `@field_validator` decorator cannot be applied to instance methods',
                code='validator-instance-method',
            )

        # auto apply the @classmethod decorator
        f = _decorators.ensure_classmethod_based_on_signature(f)

        dec_info = _decorators.FieldValidatorDecoratorInfo(
            fields=fields, mode=mode, check_fields=check_fields, json_schema_input_type=json_schema_input_type
        )
        return _decorators.PydanticDescriptorProxy(f, dec_info)

    return dec

