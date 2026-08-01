
def retrieve_all_functorch_interpreters() -> list[FuncTorchInterpreter]:
    cis = torch._C._functorch.get_interpreter_stack()
    if cis is None:
        return []
    return [coerce_cinterpreter(ci) for ci in cis]

