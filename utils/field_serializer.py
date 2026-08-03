from typing import Any, Callable

def field_serializer(
    field: str,
    /,
    *fields: str,
    mode: Literal['wrap'],
    return_type: Any = ...,
    when_used: WhenUsed = ...,
    check_fields: bool | None = ...,
) -> Callable[[_FieldWrapSerializerT], _FieldWrapSerializerT]: ...


def field_serializer(
    field: str,
    /,
    *fields: str,
    mode: Literal['plain'] = ...,
    return_type: Any = ...,
    when_used: WhenUsed = ...,
    check_fields: bool | None = ...,
) -> Callable[[_FieldPlainSerializerT], _FieldPlainSerializerT]: ...


def field_serializer(  # noqa: D417
    field: str,
    /,
    *fields: str,
    mode: Literal['plain', 'wrap'] = 'plain',
    # TODO PEP 747 (grep for 'return_type' on the whole code base):
    return_type: Any = PydanticUndefined,
    when_used: WhenUsed = 'always',
    check_fields: bool | None = None,
) -> (
    Callable[[_FieldWrapSerializerT], _FieldWrapSerializerT]
    | Callable[[_FieldPlainSerializerT], _FieldPlainSerializerT]
):
    """Decorator that enables custom field serialization.

    In the below example, a field of type `set` is used to mitigate duplication. A `field_serializer` is used to serialize the data as a sorted list.

    ```python
    from pydantic import BaseModel, field_serializer

    class StudentModel(BaseModel):
        name: str = 'Jane'
        courses: set[str]

        @field_serializer('courses', when_used='json')
        def serialize_courses_in_order(self, courses: set[str]):
            return sorted(courses)

    student = StudentModel(courses={'Math', 'Chemistry', 'English'})
    print(student.model_dump_json())
    #> {"name":"Jane","courses":["Chemistry","English","Math"]}
    ```

    See [the usage documentation](../concepts/serialization.md#serializers) for more information.

    Four signatures are supported for the decorated serializer:

    - `(self, value: Any, info: FieldSerializationInfo)`
    - `(self, value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo)`
    - `(value: Any, info: SerializationInfo)`
    - `(value: Any, nxt: SerializerFunctionWrapHandler, info: SerializationInfo)`

    Args:
        *fields: The field names the serializer should apply to.
        mode: The serialization mode.

            - `plain` means the function will be called instead of the default serialization logic,
            - `wrap` means the function will be called with an argument to optionally call the
               default serialization logic.
        return_type: Optional return type for the function, if omitted it will be inferred from the type annotation.
        when_used: Determines the serializer will be used for serialization.
        check_fields: Whether to check that the fields actually exist on the model.

    Raises:
        PydanticUserError:
            - If the decorator is used without any arguments (at least one field name must be provided).
            - If the provided field names are not strings.
    """
    if callable(field) or isinstance(field, classmethod):
        raise PydanticUserError(
            'The `@field_serializer` decorator cannot be used without arguments, at least one field must be provided. '
            "For example: `@field_serializer('<field_name>', ...)`.",
            code='decorator-missing-arguments',
        )

    fields = field, *fields
    if not all(isinstance(field, str) for field in fields):
        raise PydanticUserError(
            'The provided field names to the `@field_serializer` decorator should be strings. '
            "For example: `@field_serializer('<field_name_1>', '<field_name_2>', ...).`",
            code='decorator-invalid-fields',
        )

    def dec(f: FieldSerializer) -> _decorators.PydanticDescriptorProxy[Any]:
        dec_info = _decorators.FieldSerializerDecoratorInfo(
            fields=fields,
            mode=mode,
            return_type=return_type,
            when_used=when_used,
            check_fields=check_fields,
        )
        return _decorators.PydanticDescriptorProxy(f, dec_info)  # pyright: ignore[reportArgumentType]

    return dec  # pyright: ignore[reportReturnType]

