
def _get_buffer_names(root_module: nn.Module) -> set[str]:
    """Return the fully prefixed names of all buffers in the module hierarchy rooted at ``root_module`` as a class:`set`."""
    return {
        clean_tensor_name(buffer_name) for buffer_name, _ in root_module.named_buffers()
    }

