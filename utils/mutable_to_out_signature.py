
def mutable_to_out_signature(func: FunctionSchema) -> FunctionSchema:
    # Generating an out= schema from a mutable schema.
    if func.kind() != SchemaKind.mutable:
        raise AssertionError(f"Expected mutable schema, got {func.kind()}")
    # The new out= schema has:
    # - Any non-aliased tensor-like returns are converted to mutable, aliased out= arguments
    #   (if the argument is a tensor then we also return it for method chaining,
    #   otherwise we return nothing)
    # - an "out" overload name
    #
    # Note that:
    # (1) This also means that we can *only* generate an out= variant from a mutable schema
    #     if the mutable schema has at least one tensor-like non-aliasing return.
    # (2) The generated out= variant still has mutable positional arguments,
    #     but if necessary we could probably add another out= variant that also
    #     functionalizes the mutable arguments (a functional_out variant)

    new_returns, new_out_args = generate_out_args_from_schema(func)

    return FunctionSchema(
        name=func.name.remove_inplace().with_overload(
            get_expected_out_variant_overload_name(func.name.overload_name)
        ),
        arguments=func.arguments.with_out_args(new_out_args),
        returns=tuple(new_returns),
    )

