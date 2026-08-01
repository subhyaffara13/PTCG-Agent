
def eligible_for_binary_scalar_specialization(g: NativeFunctionsGroup) -> bool:
    num_tensors = sum(
        1 for a in g.functional.func.arguments.flat_non_out if a.type.is_tensor_like()
    )
    return num_tensors == 2

