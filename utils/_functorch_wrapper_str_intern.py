
def _functorch_wrapper_str_intern(tensor, *, tensor_contents=None):
    level = torch._C._functorch.maybe_get_level(tensor)
    if level == -1:
        raise AssertionError("expected functorch level to be >= 0, got -1")

    if torch._C._functorch.is_functionaltensor(tensor):
        # Since we're unwrapping the FunctionalTensorWrapper, we need to make sure
        # that it's up to date first
        torch._sync(tensor)

    value = torch._C._functorch.get_unwrapped(tensor)
    value_repr = repr(value)

    indented_value_repr = textwrap.indent(value_repr, " " * 4)
    if torch._C._functorch.is_batchedtensor(tensor):
        bdim = torch._C._functorch.maybe_get_bdim(tensor)
        if bdim == -1:
            raise AssertionError("expected batch dimension to be >= 0, got -1")
        return (
            f"BatchedTensor(lvl={level}, bdim={bdim}, value=\n{indented_value_repr}\n)"
        )
    if torch._C._functorch.is_gradtrackingtensor(tensor):
        return f"GradTrackingTensor(lvl={level}, value=\n{indented_value_repr}\n)"
    if torch._C._functorch.is_functionaltensor(tensor):
        return f"FunctionalTensor(lvl={level}, value=\\\n{value_repr})"

    raise ValueError("We don't know how to print this, please file us an issue")

