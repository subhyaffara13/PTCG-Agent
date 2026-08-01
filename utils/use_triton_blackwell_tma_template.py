
def use_triton_blackwell_tma_template(
    *matrices: IRNode, output_layout: Layout, add_guards: bool = False
) -> bool:
    if not use_triton_tma_template(
        *matrices, output_layout=output_layout, add_guards=add_guards
    ):
        return False

    from torch.utils._triton import has_triton_tensor_descriptor_host_tma

    from .codegen.cuda.cuda_env import is_datacenter_blackwell_arch

    # Blackwell template require the tensor descriptor API, not the experimental API.
    return has_triton_tensor_descriptor_host_tma() and is_datacenter_blackwell_arch()

