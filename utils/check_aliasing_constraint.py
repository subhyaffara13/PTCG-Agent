
def check_aliasing_constraint(name, prev, result, get_module=lambda: "???"):
    """
    custom operators' outputs must not alias any inputs or other outputs.
    """
    storages = {t.untyped_storage()._cdata for t in prev if isinstance(t, torch.Tensor)}
    tuple_result = result
    if not isinstance(result, tuple):
        tuple_result = (result,)
    for tensor in iter_tensors(tuple_result, {}):
        key = tensor.untyped_storage()._cdata
        if tensor.untyped_storage()._cdata in storages:
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
        storages.add(key)

