
def add_register_method_to_callable_class(builder: IRBuilder, fn_info: FuncInfo) -> None:
    line = fn_info.fitem.line
    with builder.enter_method(fn_info.callable_class.ir, "register", object_rprimitive):
        cls_arg = builder.add_argument("cls", object_rprimitive)
        func_arg = builder.add_argument("func", object_rprimitive, ArgKind.ARG_OPT)
        ret_val = builder.call_c(register_function, [builder.self(), cls_arg, func_arg], line)
        builder.add(Return(ret_val, line))

