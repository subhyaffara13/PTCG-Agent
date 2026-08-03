from typing import Any

def _prepare_aten_mitigations(
    aten_op: OpOverload,
    captured_args: tuple[Any, ...],
    captured_kwargs: dict[str, Any],
) -> _AtenFalsePositiveMitigations:
    """Create negated variants for aten-level false positive detection."""
    m = _AtenFalsePositiveMitigations()
    try:
        m.negated_args = _negate_tensors_in_tree(captured_args)
        m.negated_kwargs = _negate_tensors_in_tree(captured_kwargs)
        result = aten_op(*m.negated_args, **m.negated_kwargs)
        if _is_tensor_output(result):
            m.negated_ground_truth = _to_ground_truth(result)
        else:
            m.negated_args = None
            m.negated_kwargs = None
    except Exception:
        m.negated_args = None
        m.negated_kwargs = None
    return m

