
def validate_typed_dict(schema: type[TypedDictType], data: dict) -> None:
    """
    Validate that a dictionary conforms to the types defined in a TypedDict class.

    Under the hood, the typed dict is converted to a strict dataclass and validated using the `@strict` decorator.

    Args:
        schema (`type[TypedDictType]`):
            The TypedDict class defining the expected structure and types.
        data (`dict`):
            The dictionary to validate.

    Raises:
        `StrictDataclassFieldValidationError`:
            If any field in the dictionary does not conform to the expected type.

    Example:
    ```py
    >>> from typing import Annotated, TypedDict
    >>> from huggingface_hub.dataclasses import validate_typed_dict

    >>> def positive_int(value: int):
    ...     if not value >= 0:
    ...         raise ValueError(f"Value must be positive, got {value}")

    >>> class User(TypedDict):
    ...     name: str
    ...     age: Annotated[int, positive_int]

    >>> # Valid data
    >>> validate_typed_dict(User, {"name": "John", "age": 30})

    >>> # Invalid type for age
    >>> validate_typed_dict(User, {"name": "John", "age": "30"})
    huggingface_hub.errors.StrictDataclassFieldValidationError: Validation error for field 'age':
        TypeError: Field 'age' expected int, got str (value: '30')

    >>> # Invalid value for age
    >>> validate_typed_dict(User, {"name": "John", "age": -1})
    huggingface_hub.errors.StrictDataclassFieldValidationError: Validation error for field 'age':
        ValueError: Value must be positive, got -1
    ```
    """
    # Convert typed dict to dataclass
    strict_cls = _build_strict_cls_from_typed_dict(schema)

    # Validate the data by instantiating the strict dataclass
    strict_cls(**data)  # will raise if validation fails

