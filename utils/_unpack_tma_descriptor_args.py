
def _unpack_tma_descriptor_args(var_name: str, sig_type: str) -> list[str]:
    """Unpack a StableTMADescriptor into kernel launch args.

    Given a variable name holding a StableTMADescriptor and its tensordesc<...>
    signature, returns the list of pointer args: &var.m, &var.block_shape[i]...,
    &var.strides[i]...
    """
    match = re.match(r"tensordesc<[^[]*\[([^\]]*)\]", sig_type)
    assert match is not None, f"Cannot parse tensordesc signature: {sig_type}"
    ndim = match.group(1).count(",") + 1
    result = [f"&{var_name}.m"]
    for i in range(ndim):
        result.append(f"&{var_name}.block_shape[{i}]")
    for i in range(ndim):
        result.append(f"&{var_name}.strides[{i}]")
    return result

