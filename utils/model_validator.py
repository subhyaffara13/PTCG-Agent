
def model_validator(
    *,
    mode: Literal['wrap'],
) -> Callable[
    [_AnyModelWrapValidator[_ModelType]], _decorators.PydanticDescriptorProxy[_decorators.ModelValidatorDecoratorInfo]
]: ...


def model_validator(
    *,
    mode: Literal['before'],
) -> Callable[
    [_AnyModelBeforeValidator], _decorators.PydanticDescriptorProxy[_decorators.ModelValidatorDecoratorInfo]
]: ...


def model_validator(
    *,
    mode: Literal['after'],
) -> Callable[
    [_AnyModelAfterValidator[_ModelType]], _decorators.PydanticDescriptorProxy[_decorators.ModelValidatorDecoratorInfo]
]: ...


def model_validator(
    *,
    mode: Literal['wrap', 'before', 'after'],
) -> Any:
    """!!! abstract "Usage Documentation"
        [Model Validators](../concepts/validators.md#model-validators)

    Decorate model methods for validation purposes.

    Example usage:
    ```python
    from typing_extensions import Self

    from pydantic import BaseModel, ValidationError, model_validator

    class Square(BaseModel):
        width: float
        height: float

        @model_validator(mode='after')
        def verify_square(self) -> Self:
            if self.width != self.height:
                raise ValueError('width and height do not match')
            return self

    s = Square(width=1, height=1)
    print(repr(s))
    #> Square(width=1.0, height=1.0)

    try:
        Square(width=1, height=2)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Square
          Value error, width and height do not match [type=value_error, input_value={'width': 1, 'height': 2}, input_type=dict]
        '''
    ```

    For more in depth examples, see [Model Validators](../concepts/validators.md#model-validators).

    Args:
        mode: A required string literal that specifies the validation mode.
            It can be one of the following: 'wrap', 'before', or 'after'.

    Returns:
        A decorator that can be used to decorate a function to be used as a model validator.
    """

    def dec(f: Any) -> _decorators.PydanticDescriptorProxy[Any]:
        # auto apply the @classmethod decorator. NOTE: in V3, do not apply the conversion for 'after' validators:
        f = _decorators.ensure_classmethod_based_on_signature(f)
        if mode == 'after' and isinstance(f, classmethod):
            warnings.warn(
                category=PydanticDeprecatedSince212,
                message=(
                    "Using `@model_validator` with mode='after' on a classmethod is deprecated. Instead, use an instance method. "
                    f'See the documentation at https://docs.pydantic.dev/{version_short()}/concepts/validators/#model-after-validator.'
                ),
                stacklevel=2,
            )

        dec_info = _decorators.ModelValidatorDecoratorInfo(mode=mode)
        return _decorators.PydanticDescriptorProxy(f, dec_info)

    return dec

