
def _reconstruct_closure_fn(stripped, extracted_leaves, closure_spec):
    """Rebuild a function from a _StrippedClosure and flattened extracted leaves."""
    if not isinstance(stripped, _StrippedClosure):
        return stripped

    all_leaves: list[BaseArgumentTypes | Callable[..., Any]] = []
    idx = 0
    for entry in stripped.leaf_entries:
        if isinstance(entry, _FunctionLeaf):
            child_fn = _reconstruct_closure_fn(
                entry.stripped,
                extracted_leaves[idx : idx + entry.n_extracted],
                entry.closure_spec,
            )
            all_leaves.append(child_fn)
            idx += entry.n_extracted
        else:
            # _EXTRACTED_LEAF — take from extracted leaves
            all_leaves.append(extracted_leaves[idx])
            idx += 1

    contents = tree_unflatten(all_leaves, closure_spec)
    new_cells = tuple(types.CellType(v) for v in contents)

    restored = types.FunctionType(
        stripped.code,
        stripped.globals_dict,
        stripped.name,
        stripped.defaults,
        new_cells,
    )
    restored.__qualname__ = stripped.qualname
    if stripped.kwdefaults:
        restored.__kwdefaults__ = stripped.kwdefaults
    if stripped.extra_dict:
        restored.__dict__.update(stripped.extra_dict)

    return restored

