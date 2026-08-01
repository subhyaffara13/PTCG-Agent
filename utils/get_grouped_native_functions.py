
def get_grouped_native_functions(
    native_functions: Sequence[NativeFunction],
) -> Sequence[NativeFunction | NativeFunctionsGroup]:
    def flatten_pre_group(
        d: dict[SchemaKind, NativeFunction],
    ) -> Sequence[NativeFunction | NativeFunctionsGroup]:
        r = NativeFunctionsGroup.from_dict(d)
        if r is None:
            # Invariant: any NativeFunctions that are code-generated
            # should have been grouped into NativeFunctionsGroup objects
            if any("generated" in f.tags for f in d.values()):
                raise AssertionError(
                    "Generated NativeFunctions should have been grouped into "
                    f"NativeFunctionsGroup objects: {list(d.values())}"
                )
            return list(d.values())
        else:
            return [r]

    # TODO: how come ValuesView isn't a Sequence lol
    pre_grouped_native_functions = pre_group_native_functions(native_functions)
    return list(
        concatMap(flatten_pre_group, list(pre_grouped_native_functions.values()))
    )

