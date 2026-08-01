
def inferred_fake_kernel_from_real_out(
    mode: FakeTensorMode, op: torch._ops.OpOverload, real_out: Any
) -> Any:
    if mode.shape_env is None:
        raise AssertionError("mode.shape_env must not be None")

    # Only support operators that have all Tensor outputs
    # This is a general limitation on custom ops that we impose for PT2
    # to avoid baking non-symbolic float/int outputs into the graph.
    real_flat_out, spec = pytree.tree_flatten(real_out)
    if not all(isinstance(t, torch.Tensor) for t in real_flat_out):
        raise RuntimeError(
            f"propagate_real_tensors: we don't support operators that return "
            f"non-Tensors. Got {op._schema}"
        )

    fake_flat_out = [_infer_fake_from_real_tensor(mode, op, t) for t in real_flat_out]
    return pytree.tree_unflatten(fake_flat_out, spec)

