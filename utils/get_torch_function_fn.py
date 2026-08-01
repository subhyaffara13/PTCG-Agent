
def get_torch_function_fn(
    tx: "InstructionTranslator", vt: VariableTracker
) -> VariableTracker:
    # The underlying function could be a classmethod, staticmethod, regular
    # function or a function with C-implementation. It doesn't matter as long as
    # they satisfy the calling convention in `call_torch_function`.

    args = [vt, VariableTracker.build(tx, "__torch_function__")]
    func_vt = VariableTracker.build(tx, getattr).call_function(tx, args, {})
    return func_vt

