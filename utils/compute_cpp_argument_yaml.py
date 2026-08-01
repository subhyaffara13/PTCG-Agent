
def compute_cpp_argument_yaml(
    cpp_a: Binding,
    *,
    schema_order: bool,
    kwarg_only_set: set[str],
    out_arg_set: set[str],
    name_to_field_name: dict[str, str],
) -> object:
    if isinstance(cpp_a.argument, TensorOptionsArguments):
        arg: dict[str, object] = {
            "annotation": None,
            "dynamic_type": "at::TensorOptions",
            "is_nullable": False,
            "name": cpp_a.name,
            "type": cpp_a.type,
            "kwarg_only": True,
        }
        if cpp_a.default is not None:
            arg["default"] = cpp_a.default
        return arg
    elif isinstance(cpp_a.argument, SelfArgument):
        raise AssertionError
    elif isinstance(cpp_a.argument, Argument):
        return compute_argument_yaml(
            cpp_a.argument,
            schema_order=schema_order,
            kwarg_only_set=kwarg_only_set,
            out_arg_set=out_arg_set,
            name_to_field_name=name_to_field_name,
        )

