
def build_fingerprint_fast(fn_args_vt: Any) -> InputFingerprint:
    """Build fingerprint for the common case of flat leaf args, no kwargs."""
    flat_vts: list[tuple[InputTag, VariableTracker]] = []
    arg_sources: list[Source | None] = []
    for vt in fn_args_vt:
        tag = classify_vt(vt)
        assert tag is not None
        flat_vts.append((tag, vt))
        # Always append (even None) to keep positional alignment with flat_vts
        # so that source_replacement zip pairing is correct across calls.
        arg_sources.append(getattr(vt, "source", None))
    return InputFingerprint(flat_vts, arg_sources)

