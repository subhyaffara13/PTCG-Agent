from typing import Callable

def make_signal_windows_opinfo(
    name: str,
    ref: Callable,
    sample_inputs_func: Callable,
    reference_inputs_func: Callable,
    error_inputs_func: Callable,
    *,
    skips: tuple[DecorateInfo, ...] = (),
):
    r"""Helper function to create OpInfo objects related to different windows."""
    return OpInfo(
        name=name,
        ref=ref if TEST_SCIPY else None,
        dtypes=floating_types(),
        sample_inputs_func=sample_inputs_func,
        reference_inputs_func=reference_inputs_func,
        error_inputs_func=error_inputs_func,
        supports_out=False,
        supports_autograd=False,
        skips=(
            # TODO: same as this?
            # https://github.com/pytorch/pytorch/issues/81774
            # also see: arange, new_full
            # fails to match any schemas despite working in the interpreter
            DecorateInfo(
                unittest.expectedFailure,
                "TestOperatorSignatures",
                "test_get_torch_func_signature_exhaustive",
            ),
            # fails to match any schemas despite working in the interpreter
            DecorateInfo(
                unittest.expectedFailure, "TestJit", "test_variant_consistency_jit"
            ),
            # skip these tests since we have non tensor input
            DecorateInfo(
                unittest.skip("Skipped!"), "TestCommon", "test_noncontiguous_samples"
            ),
            DecorateInfo(
                unittest.skip("Skipped!"),
                "TestCommon",
                "test_variant_consistency_eager",
            ),
            DecorateInfo(unittest.skip("Skipped!"), "TestMathBits", "test_conj_view"),
            DecorateInfo(
                unittest.skip("Skipped!"), "TestMathBits", "test_neg_conj_view"
            ),
            DecorateInfo(unittest.skip("Skipped!"), "TestMathBits", "test_neg_view"),
            DecorateInfo(
                unittest.skip("Skipped!"),
                "TestVmapOperatorsOpInfo",
                "test_vmap_exhaustive",
            ),
            DecorateInfo(
                unittest.skip("Skipped!"),
                "TestVmapOperatorsOpInfo",
                "test_op_has_batch_rule",
            ),
            DecorateInfo(
                unittest.skip("Buggy on MPS for now (mistakenly promotes to float64)"),
                "TestCommon",
                "test_numpy_ref_mps",
            ),
            *skips,
        ),
    )

