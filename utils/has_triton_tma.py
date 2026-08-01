
def has_triton_tma() -> bool:
    return has_triton_tensor_descriptor_host_tma() or has_triton_experimental_host_tma()

