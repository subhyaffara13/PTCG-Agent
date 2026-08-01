
def pre_group_native_functions(
    native_functions: Sequence[NativeFunction],
) -> dict[FunctionSchema, dict[SchemaKind, NativeFunction]]:
    pre_grouped_native_functions: dict[
        FunctionSchema, dict[SchemaKind, NativeFunction]
    ] = defaultdict(dict)
    for f in native_functions:
        d = pre_grouped_native_functions[f.func.signature()]
        if f.func.kind() in d:
            raise AssertionError(f"Duplicate schema kind {f.func.kind()} for {f.func}")
        d[f.func.kind()] = f
    return pre_grouped_native_functions

