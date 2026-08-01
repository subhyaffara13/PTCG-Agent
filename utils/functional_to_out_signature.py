
def functional_to_out_signature(func: FunctionSchema) -> FunctionSchema:
    # Generating an out= schema from a functional schema.
    if func.kind() != SchemaKind.functional:
        raise AssertionError(f"Expected functional schema, got {func.kind()}")

    new_returns, new_out_args = generate_out_args_from_schema(func)
    # The new out= schema has:
    # - one or more new out argument(s) with the same type as returns (but with a mutable annotation)
    # - The returns now alias the out= arguments
    # - an "_out" overload name
    return FunctionSchema(
        name=func.name.with_overload(
            get_expected_out_variant_overload_name(func.name.overload_name)
        ),
        arguments=func.arguments.signature().with_out_args(
            new_out_args,
        ),
        returns=tuple(new_returns),
    )

