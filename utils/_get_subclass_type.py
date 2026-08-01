
def _get_subclass_type(var: VariableTracker) -> type:
    assert isinstance(var, (TensorWithTFOverrideVariable, UserDefinedObjectVariable))
    return var.python_type()

