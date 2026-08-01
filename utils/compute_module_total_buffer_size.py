
def compute_module_total_buffer_size(model: nn.Module, hf_quantizer: "HfQuantizer | None" = None):
    """
    Compute the total size of buffers in each submodule of a given model.
    """
    module_sizes, _ = compute_module_sizes(model, hf_quantizer, buffers_only=True)
    return module_sizes.get("", 0)

