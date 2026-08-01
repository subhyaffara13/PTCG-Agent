
def gen_annotated_args(f: NativeFunction) -> str:
    def _get_kwargs_func_exclusion_list() -> list[str]:
        # functions that currently don't work with kwargs in test_overrides.py
        return [
            "diagonal",
            "round_",
            "round",
            "scatter_",
        ]

    def _add_out_arg(
        out_args: list[dict[str, Any]], args: Sequence[Argument], *, is_kwarg_only: bool
    ) -> None:
        for arg in args:
            if arg.default is not None:
                continue
            out_arg: dict[str, Any] = {}
            out_arg["is_kwarg_only"] = str(is_kwarg_only)
            out_arg["name"] = arg.name
            out_arg["simple_type"] = python.argument_type_str(
                arg.type, simple_type=True
            )
            size_t = python.argument_type_size(arg.type)
            if size_t:
                out_arg["size"] = size_t
            out_args.append(out_arg)

    out_args: list[dict[str, Any]] = []
    _add_out_arg(out_args, f.func.arguments.flat_positional, is_kwarg_only=False)
    if f"{f.func.name.name}" not in _get_kwargs_func_exclusion_list():
        _add_out_arg(out_args, f.func.arguments.flat_kwarg_only, is_kwarg_only=True)

    return f"{f.func.name.name}: {repr(out_args)},"

