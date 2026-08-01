
def add_await_to_generator_class(builder: IRBuilder, fn_info: FuncInfo) -> None:
    """Generates the '__await__' method for a generator class."""
    with builder.enter_method(fn_info.generator_class.ir, "__await__", object_rprimitive, fn_info):
        builder.add(Return(builder.self()))

