
def is_reference_for_foreach(
    f: NativeFunction,
    function_schema: FunctionSchema,
) -> bool:
    return (
        f.func.name.name.base.split("_foreach_")[-1] == function_schema.name.name.base
        and (
            not function_schema.name.name.inplace
            or str(f.func.name) in _foreach_with_inplace_ref
        )
        and (
            str(f.func.name) in _skip_argument_len_check
            or len(f.func.arguments.flat_non_out)
            == len(function_schema.arguments.flat_non_out)
        )
        and all(
            ref_arg.type in (arg.type, getattr(arg.type, "elem", None))
            for arg, ref_arg in zip(
                f.func.arguments.flat_non_out,
                function_schema.arguments.flat_non_out,
            )
        )
    )

