
def var_object_size(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    elem_address = builder.add(GetElementPtr(args[0], PyVarObject, "ob_size"))
    return builder.add(LoadMem(c_pyssize_t_rprimitive, elem_address, line))

