
def transform_overloaded_func_def(builder: IRBuilder, o: OverloadedFuncDef) -> None:
    # Handle regular overload case
    assert o.impl
    builder.accept(o.impl)

