
def create_call_function(nargs: int, push_null: bool) -> list[Instruction]:
    """
    Creates a sequence of instructions that makes a function call.

    `push_null` is used in Python 3.11+ only. It is used in codegen when
    a function call is intended to be made with the NULL + fn convention,
    and we know that the NULL has not been pushed yet. We will push a
    NULL and rotate it to the correct position immediately before making
    the function call.

    `push_null` should be True if no NULL is pushed for the callable.
    Conversely, `push_null` should be False if a NULL was pushed for the callable.
    Prefer using `push_null=False` when possible since we will not need to rotate
    NULL to the right place, which is less efficient.

    Generally, you should codegen a function by using `add_push_null` then
    `create_call_function` with `push_null=False`.

    Example of when to set push_null False:

    insts = [
        create_instruction("LOAD_GLOBAL", argval="torch"),
        create_instruction("LOAD_ATTR", argval="nn"),
        create_instruction("LOAD_ATTR", argval="functional"),
        create_instruction("LOAD_ATTR", argval="relu"),
    ]
    insts = add_push_null(insts)
    insts.append(create_instruction("LOAD_FAST", argval="x"))
    insts.extend(create_call_function(1, False))

    Example of when to set push_null True:

    insts = [create_instruction("LOAD_FAST", x)]
    for should_wrap, wrapper_name in wrappers:
        if should_wrap:
            insts.extend([
                create_instruction("LOAD_GLOBAL", argval="wrapper1"),
                create_instruction("SWAP", arg=2),
                *create_call_function(1, True),
            )
    """
    if sys.version_info >= (3, 11):
        output = []
        if push_null:
            output.append(create_instruction("PUSH_NULL"))
            # 3.13 swapped NULL and callable
            rots = nargs + 1 if sys.version_info >= (3, 13) else nargs + 2
            output.extend(create_rot_n(rots))
        if sys.version_info < (3, 12):
            output.append(create_instruction("PRECALL", arg=nargs))
        output.append(create_instruction("CALL", arg=nargs))
        return output
    return [create_instruction("CALL_FUNCTION", arg=nargs)]

