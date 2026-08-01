
def classify_vt(vt: Any) -> InputTag | None:
    """Return the tag for a leaf VT, or None if unsupported."""
    if isinstance(vt, TensorVariable):
        return InputTag.TENSOR
    elif isinstance(vt, SymNodeVariable):
        return InputTag.SYMNODE
    elif isinstance(vt, ConstantVariable):
        return InputTag.CONSTANT
    elif isinstance(vt, UnspecializedNNModuleVariable):
        return InputTag.MODULE
    return None

