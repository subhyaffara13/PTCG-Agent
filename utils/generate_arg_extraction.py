
def generate_arg_extraction(schema: FunctionSchema) -> str:
    arg_populations = []
    for i, arg in enumerate(schema.schema_order_arguments()):
        maybe_method = ivalue_type_conversion_method(arg.type)
        if not maybe_method:
            raise AssertionError(
                f"No type conversion method for {arg.name}: {arg.type}"
            )
        is_reference, type_conversion_method = maybe_method
        reference = "&" if is_reference else ""
        arg_populations.append(
            f"const auto{reference} {arg.name} = p_node->Input({i}).{type_conversion_method}"
        )
    return ";\n    ".join(arg_populations) + ";"

