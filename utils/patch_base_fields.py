
def patch_base_fields(cls: type[Any]) -> Generator[None]:
    """Temporarily patch the stdlib dataclasses bases of `cls` if the Pydantic `Field()` function is used.

    When creating a Pydantic dataclass, it is possible to inherit from stdlib dataclasses, where
    the Pydantic `Field()` function is used. To create this Pydantic dataclass, we first apply
    the stdlib `@dataclass` decorator on it. During the construction of the stdlib dataclass,
    the `kw_only` and `repr` field arguments need to be understood by the stdlib *during* the
    dataclass construction. To do so, we temporarily patch the fields dictionary of the affected
    bases.

    For instance, with the following example:

    ```python {test="skip" lint="skip"}
    import dataclasses as stdlib_dc

    import pydantic
    import pydantic.dataclasses as pydantic_dc

    @stdlib_dc.dataclass
    class A:
        a: int = pydantic.Field(repr=False)

    # Notice that the `repr` attribute of the dataclass field is `True`:
    A.__dataclass_fields__['a']
    #> dataclass.Field(default=FieldInfo(repr=False), repr=True, ...)

    @pydantic_dc.dataclass
    class B(A):
        b: int = pydantic.Field(repr=False)
    ```

    When passing `B` to the stdlib `@dataclass` decorator, it will look for fields in the parent classes
    and reuse them directly. When this context manager is active, `A` will be temporarily patched to be
    equivalent to:

    ```python {test="skip" lint="skip"}
    @stdlib_dc.dataclass
    class A:
        a: int = stdlib_dc.field(default=Field(repr=False), repr=False)
    ```

    !!! note
        This is only applied to the bases of `cls`, and not `cls` itself. The reason is that the Pydantic
        dataclass decorator "owns" `cls` (in the previous example, `B`). As such, we instead modify the fields
        directly (in the previous example, we simply do `setattr(B, 'b', as_dataclass_field(pydantic_field))`).

    !!! note
        This approach is far from ideal, and can probably be the source of unwanted side effects/race conditions.
        The previous implemented approach was mutating the `__annotations__` dict of `cls`, which is no longer a
        safe operation in Python 3.14+, and resulted in unexpected behavior with field ordering anyway.
    """
    # A list of two-tuples, the first element being a reference to the
    # dataclass fields dictionary, the second element being a mapping between
    # the field names that were modified, and their original `Field`:
    original_fields_list: list[tuple[DcFields, DcFields]] = []

    for base in cls.__mro__[1:]:
        dc_fields: dict[str, dataclasses.Field[Any]] = base.__dict__.get('__dataclass_fields__', {})
        dc_fields_with_pydantic_field_defaults = {
            field_name: field
            for field_name, field in dc_fields.items()
            if isinstance(field.default, FieldInfo)
            # Only do the patching if one of the affected attributes is set:
            and (field.default.description is not None or field.default.kw_only or field.default.repr is not True)
        }
        if dc_fields_with_pydantic_field_defaults:
            original_fields_list.append((dc_fields, dc_fields_with_pydantic_field_defaults))
            for field_name, field in dc_fields_with_pydantic_field_defaults.items():
                default = cast(FieldInfo, field.default)
                # `dataclasses.Field` isn't documented as working with `copy.copy()`.
                # It is a class with `__slots__`, so should work (and we hope for the best):
                new_dc_field = copy.copy(field)
                # For base fields, no need to set `doc` from `FieldInfo.description`, this is only relevant
                # for the class under construction and handled in `as_dataclass_field()`.
                if sys.version_info >= (3, 10) and default.kw_only:
                    new_dc_field.kw_only = True
                if default.repr is not True:
                    new_dc_field.repr = default.repr
                dc_fields[field_name] = new_dc_field

    try:
        yield
    finally:
        for fields, original_fields in original_fields_list:
            for field_name, original_field in original_fields.items():
                fields[field_name] = original_field

