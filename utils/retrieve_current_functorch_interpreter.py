
def retrieve_current_functorch_interpreter() -> FuncTorchInterpreter:
    interpreter = torch._C._functorch.peek_interpreter_stack()
    if interpreter is None:
        raise AssertionError("interpreter must not be None")
    return coerce_cinterpreter(interpreter)

