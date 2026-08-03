from typing import Any

def str_schema(
    *,
    pattern: str | Pattern[str] | None = None,
    max_length: int | None = None,
    min_length: int | None = None,
    strip_whitespace: bool | None = None,
    to_lower: bool | None = None,
    to_upper: bool | None = None,
    regex_engine: Literal['rust-regex', 'python-re'] | None = None,
    strict: bool | None = None,
    coerce_numbers_to_str: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> StringSchema:
    """
    Returns a schema that matches a string value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.str_schema(max_length=10, min_length=2)
    v = SchemaValidator(schema)
    assert v.validate_python('hello') == 'hello'
    ```

    Args:
        pattern: A regex pattern that the value must match
        max_length: The value must be at most this length
        min_length: The value must be at least this length
        strip_whitespace: Whether to strip whitespace from the value
        to_lower: Whether to convert the value to lowercase
        to_upper: Whether to convert the value to uppercase
        regex_engine: The regex engine to use for pattern validation. Default is 'rust-regex'.
            - `rust-regex` uses the [`regex`](https://docs.rs/regex) Rust
              crate, which is non-backtracking and therefore more DDoS
              resistant, but does not support all regex features.
            - `python-re` use the [`re`](https://docs.python.org/3/library/re.html) module,
              which supports all regex features, but may be slower.
        strict: Whether the value should be a string or a value that can be converted to a string
        coerce_numbers_to_str: Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='str',
        pattern=pattern,
        max_length=max_length,
        min_length=min_length,
        strip_whitespace=strip_whitespace,
        to_lower=to_lower,
        to_upper=to_upper,
        regex_engine=regex_engine,
        strict=strict,
        coerce_numbers_to_str=coerce_numbers_to_str,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

