
def _load_tuple_and_call(tup: tuple[Any, ...]) -> list[Instruction]:
    insts: list[Instruction] = []
    _initial_push_null(insts)
    insts.extend(create_load_const(val) for val in tup)
    insts.extend(create_call_function(len(tup), False))
    return insts

