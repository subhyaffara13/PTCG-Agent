
def tree_flatten_spec(
    pytree: PyTree,
    spec: TreeSpec,
) -> list[Any]:
    if spec.is_leaf():
        return [pytree]
    # I guess these exist for BC, FC reasons.
    # In general, we should be able to directly
    # use pytree tree flattener to flatten them,
    # as export serializes the pytree separately.
    # Will remove it in follow up PR.
    if spec.type in SUPPORTED_NODES:
        flatten_fn_spec = SUPPORTED_NODES[spec.type]
        child_pytrees = flatten_fn_spec(pytree, spec)
        result: list[Any] = []
        for child, child_spec in zip(child_pytrees, spec.children()):
            flat = tree_flatten_spec(child, child_spec)
            result += flat
        return result
    flat_result, real_spec = tree_flatten(pytree)
    if spec != real_spec:
        raise RuntimeError(
            f"Real spec {real_spec} of object {pytree} is different from expected spec {spec}. "
            f"Please file an issue at https://github.com/pytorch/pytorch/issues/new?template=bug-report.yml"
        )
    return flat_result

