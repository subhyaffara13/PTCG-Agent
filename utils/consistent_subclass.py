
def consistent_subclass(out, in_):
    # For ndarray subclass input, our output should have the same subclass
    # (non-ndarray input gets converted to ndarray).
    return type(out) is (type(in_) if isinstance(in_, np.ndarray)
                         else np.ndarray)

