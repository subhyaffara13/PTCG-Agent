
def scatter_upon_const_tensor(
    match: Match, shape, background_val, dtype, dim, selector, val
):
    """
    Match the pattern of full+scatter into a pointwise operation in joint graph.

    TODO: Right now the scatter value must be a scalar. But we could support it
    when it is a tensor as well.
    """
    from torch._inductor import metrics

    # pyrefly: ignore  # bad-assignment
    metrics.num_matches_for_scatter_upon_const_tensor += 1

    # Create a replacement that uses torch.where for the pointwise operation
    def repl_fn(shape, background_val, dim, selector, val):
        # Create a tensor of indices for the scatter dimension
        length = shape[dim]
        indices = torch.arange(length, device=selector.device, dtype=torch.int64)

        # Reshape indices to have size 'length' at dim, then broadcast
        view_shape = [1] * len(shape)
        view_shape[dim] = length
        indices_view = indices.view(*view_shape)

        # Broadcast selector to match full tensor shape
        selector_expanded = selector.expand(shape)

        # Create a mask for where to scatter
        mask = selector_expanded == indices_view

        # Use torch.where to implement the scatter pointwise operation
        return torch.where(mask, val, background_val)

    # replace the scatter operation with pointwise equivalent
    # pyrefly: ignore [bad-argument-type]
    match.replace_by_example(repl_fn, [shape, background_val, dim, selector, val])

