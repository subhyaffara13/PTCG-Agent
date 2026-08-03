import os

def _sample_inputs_sparse(
    sample_inputs,
    maybe_failing_sample_inputs,
    validate_sample_input,
    op_info,
    *args,
    **kwargs,
):
    check_validate = (
        os.environ.get("PYTORCH_TEST_CHECK_VALIDATE_SPARSE_SAMPLES", "0") == "1"
    )
    for sample in sample_inputs(op_info, *args, **kwargs):
        sample = validate_sample_input(op_info, sample, check_validate=check_validate)
        if isinstance(sample, SampleInput):
            yield sample
        # Error inputs are handled in error_inputs_sparse

    for sample in maybe_failing_sample_inputs(op_info, *args, **kwargs):
        sample = validate_sample_input(op_info, sample, check_validate=check_validate)
        if isinstance(sample, SampleInput):
            yield sample

