
def buf_init_item(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    """Initialize an item in a buffer of "PyObject *" values at given index.

    This can be used to initialize the data buffer of a freshly allocated list
    object.
    """
    base = args[0]
    index_value = args[1]
    value = args[2]
    assert isinstance(index_value, Integer), index_value
    index = index_value.numeric_value()
    if index == 0:
        ptr = base
    else:
        ptr = builder.add(
            IntOp(
                pointer_rprimitive,
                base,
                Integer(index * PLATFORM_SIZE, c_pyssize_t_rprimitive),
                IntOp.ADD,
                line,
            )
        )
    return builder.add(SetMem(object_rprimitive, ptr, value, line))

