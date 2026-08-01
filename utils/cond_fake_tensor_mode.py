
def cond_fake_tensor_mode(mode, pred, true_fn, false_fn, operands):
    # Ignore here, because if you've gotten here but you're not manually
    # tracing the inner graphs, that means that you intend to reuse the graph
    # directly.  Which means the old unbacked symbol bindings are appropriate.
    # This strategy will not work if unbacked symbols can escape.
    ignore_fresh_unbacked = contextlib.nullcontext()
    if mode.shape_env:
        ignore_fresh_unbacked = mode.shape_env.ignore_fresh_unbacked_symbols()

    with mode, ignore_fresh_unbacked:
        flat_true_outs, true_out_spec = pytree.tree_flatten(true_fn(*operands))
        flat_false_outs, false_out_spec = pytree.tree_flatten(false_fn(*operands))
        if true_out_spec != false_out_spec:
            raise RuntimeError(
                "Unmatched output spec from torch.cond branches: "
                f"true branch tree_spec {true_out_spec} vs false branch tree_spec {false_out_spec}."
            )

    merged_outs = []
    for true_out, false_out in zip(flat_true_outs, flat_false_outs):
        merged_outs.append(_merge_output(true_out, false_out, mode))
    return pytree.tree_unflatten(merged_outs, true_out_spec)

