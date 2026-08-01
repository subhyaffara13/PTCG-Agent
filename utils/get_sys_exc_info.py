
def get_sys_exc_info(builder: IRBuilder) -> list[Value]:
    line = builder.fn_info.fitem.line
    exc_info = builder.call_c(get_exc_info_op, [], line)
    return [builder.add(TupleGet(exc_info, i, line)) for i in range(3)]

