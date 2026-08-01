
def root_module_when_exporting_non_strict(
    flat_fn: Callable[..., Any],
) -> torch.nn.Module | None:
    # When exporting in non-strict mode, we wrap the root module in a specific pattern.
    # See `_aot_export_non_strict` in torch.export._trace.py.
    # We look for that wrapping pattern here.
    if hasattr(flat_fn, "_orig_mod") and hasattr(flat_fn._orig_mod, "_export_root"):
        return flat_fn._orig_mod._export_root
    else:
        return None

