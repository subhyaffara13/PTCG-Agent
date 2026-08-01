
def check_metadata_matches(n: object, r: object, desc: Callable[[], str]) -> None:
    if not callable(desc):
        raise AssertionError(f"desc must be callable, got {type(desc)}")
    n_vals, _n_spec = pytree.tree_flatten(n)
    r_vals, _r_spec = pytree.tree_flatten(r)
    # TODO: test the specs match; empirically  sometimes we have a tuple
    # on one side and a list on the other
    if len(n_vals) != len(r_vals):
        raise AssertionError(f"{len(n_vals)} != {len(r_vals)}")
    for i, nv, rv in zip(range(len(n_vals)), n_vals, r_vals):
        if not isinstance(rv, torch.Tensor):
            continue
        check_tensor_metadata_matches(nv, rv, lambda: f"{desc()} output {i}")

