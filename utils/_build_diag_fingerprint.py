
def _build_diag_fingerprint(
    gm: torch.fx.GraphModule,
) -> tuple[tuple[str, str | None], ...]:
    """Build human-readable fingerprint for mismatch diagnostics.

    Only called on the rare mismatch path.
    """
    from torch._inductor.codecache import extract_tensor_metadata_for_cache_key

    entries: list[tuple[str, str | None]] = []
    for n in gm.graph.nodes:
        if n.op != "call_function":
            continue
        target_str = str(n.target)
        val = n.meta.get("val")
        entries.append(
            (
                target_str,
                _format_val_metadata(val, extract_tensor_metadata_for_cache_key),
            )
        )
    return tuple(entries)

