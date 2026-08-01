
def _get_subclass_type_var(
    tx: "InstructionTranslator", var: VariableTracker
) -> VariableTracker:
    if isinstance(var, TensorWithTFOverrideVariable):
        return var.class_type_var(tx)
    elif isinstance(var, UserDefinedObjectVariable):
        source = var.source and TypeSource(var.source)
        return VariableTracker.build(tx, var.python_type(), source)
    else:
        raise AssertionError(f"Unexpected type {type(var)}")

