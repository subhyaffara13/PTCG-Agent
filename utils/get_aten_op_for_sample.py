
def get_aten_op_for_sample(
    op: Callable[..., Any], sample: SampleInput, op_name: str = ""
) -> _CaptureAtenOp:
    """
    Capture aten ops dispatched for a given sample.

    Returns the _CaptureAtenOp object containing all captured ops with their
    args, kwargs, and return values. Use best_match for the primary op or
    all_ops for exhaustive iteration.
    """
    with _CaptureAtenOp(op_name) as capture:
        try:
            if isinstance(sample.input, torch.Tensor):
                op(sample.input, *sample.args, **sample.kwargs)
            else:
                op(*sample.input, *sample.args, **sample.kwargs)
        except Exception:
            pass

    # Populate best_match from first op if target match wasn't found
    if capture.best_match is None and capture.all_ops:
        first_op, first_args, first_kwargs, first_result = capture.all_ops[0]
        capture.best_match = first_op
        capture.best_match_args = first_args
        capture.best_match_kwargs = first_kwargs
        capture.best_match_result = first_result

    return capture

