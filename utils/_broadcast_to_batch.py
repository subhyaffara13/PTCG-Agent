
def _broadcast_to_batch(output, batch_size):
    """Expand each tensor in output pytree to include batch dimension.

    Note: Although outputs are flattened in the compiled path (via torch.compile),
    users may call map_impl directly with pytree outputs, so we support pytrees
    for backward compatibility.
    """

    def expand_with_batch(t):
        if isinstance(t, torch.Tensor):
            # Use contiguous_format to match torch.stack behavior
            return (
                t.unsqueeze(0)
                .expand(batch_size, *t.shape)
                .clone(memory_format=torch.contiguous_format)
            )
        return t

    return pytree.tree_map(expand_with_batch, output)

