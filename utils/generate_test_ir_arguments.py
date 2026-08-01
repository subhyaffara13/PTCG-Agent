
def generate_test_ir_arguments(
    schema: FunctionSchema,
) -> list[tuple[str, str | None]]:
    def ir_argument(arg: Argument) -> tuple[str, str | None]:
        t = arg.type
        add_optional = False
        if isinstance(t, OptionalType):
            t = t.elem
            add_optional = True
        if not isinstance(t, BaseType):
            raise AssertionError(f"Expected BaseType, got {type(t)}")
        type_str = None
        if t.name in generate_test_ir_arguments_base_ty_to_type_str_:
            type_str = generate_test_ir_arguments_base_ty_to_type_str_[t.name]
        if type_str and add_optional:
            type_str = f"{type_str}?"
        return ("%" + arg.name, type_str)

    return [ir_argument(arg) for arg in schema.schema_order_arguments()]

