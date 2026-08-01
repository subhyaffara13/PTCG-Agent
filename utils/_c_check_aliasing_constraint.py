
def _c_check_aliasing_constraint(name, args, kwargs, result, get_module=lambda: "???"):
    """
    custom operators' outputs must not have any aliases
    This version uses C++ implementation for perf.
    Only List container is supported.
    Tensors in Lists with not only Tensors are checked.
    """
    tuple_result = result
    if not isinstance(result, tuple):
        tuple_result = (result,)
    if _C._any_output_is_alias_to_input_or_output(args, kwargs, tuple_result):
        raise RuntimeError(
            f"{name} (with implementation in {get_module()}): "
            f"The output of this custom operator (1) must not "
            f"also be an input to this custom operator and "
            f"(2) may not alias any inputs to this custom operator "
            f"or other returns. "
            f"The most common way to trigger this error is if "
            f"we have y = custom_op(x) and y and x are the same Tensor. "
            f"Please instead return a clone of the offending output "
            f"tensor(s) (e.g. return x.clone()) or refactor the custom "
            f"operator to not return y."
        )

