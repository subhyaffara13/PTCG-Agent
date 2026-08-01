
def get_triton_kernels_for_op(name: str) -> list[object]:
    return triton_ops_to_kernels.get(name, [])

