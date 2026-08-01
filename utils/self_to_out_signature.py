
def self_to_out_signature(func: FunctionSchema) -> FunctionSchema:
    # Generating an out= schema from an inplace schema.
    if func.kind() != SchemaKind.inplace:
        raise AssertionError(f"Expected inplace schema, got {func.kind()}")
    if func.arguments.self_arg is None:
        raise AssertionError("Expected self_arg to be non-None")
    # The new out= schema has:
    # - a new out argument with the same type as "func" (but with a mutable annotation)
    # - The returns (if any) now alias the out= argument instead of "func"
    # - an "out" overload name
    return FunctionSchema(
        name=func.name.remove_inplace().with_overload(
            get_expected_out_variant_overload_name(func.name.overload_name)
        ),
        arguments=func.arguments.remove_self_annotation().with_out_args(
            [
                Argument(
                    name="out",
                    type=func.arguments.self_arg.argument.type,
                    default=None,
                    annotation=func.arguments.self_arg.argument.annotation,
                )
            ]
        ),
        returns=func.returns,
    )

