
def trace_reuse_hash_fn(
    tx: "InstructionTranslator",
    reuse_hash_fn: Any,
    fn_args_vt: "Sequence[VariableTracker]",
    kwargs: dict[str, VariableTracker],
) -> int:
    """Trace the user's reuse_hash_fn to get a constant integer hash key.

    Guards installed during the hash function tracing are skipped — the hash
    key itself is the reuse condition, not the guards.
    """
    from torch._dynamo.exc import Unsupported
    from torch._dynamo.utils import _make_inlined

    with tx.output.tracing_context.guards_context.skip_guard_install():
        try:
            result = _make_inlined(tx, reuse_hash_fn)(*fn_args_vt, **kwargs)
        except Unsupported as e:
            raise RuntimeError(
                f"reuse_hash_fn must be fully traceable without graph breaks. Got: {e}"
            ) from e

    if not isinstance(result, ConstantVariable) or not isinstance(result.value, int):
        raise RuntimeError(
            f"reuse_hash_fn must return a constant integer, got {result}"
        )

    return result.value

