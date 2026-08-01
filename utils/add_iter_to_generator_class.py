
def add_iter_to_generator_class(builder: IRBuilder, fn_info: FuncInfo) -> None:
    """Generates the '__iter__' method for a generator class."""
    with builder.enter_method(fn_info.generator_class.ir, "__iter__", object_rprimitive, fn_info):
        builder.add(Return(builder.self()))

