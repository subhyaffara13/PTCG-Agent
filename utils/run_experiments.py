
def run_experiments(use_fp16, batch_size, is_baseline=False):
    """Run experiments to compare different algorithms on one batch size"""
    test_results = run_tests(
        use_fp16=use_fp16,
        use_merged_qkv_weights=True,
        use_half4=False,
        batch_size=batch_size,
    )

    if is_baseline:
        return test_results

    if use_fp16:
        test_results += run_tests(
            use_fp16=use_fp16,
            use_merged_qkv_weights=True,
            use_half4=True,
            batch_size=batch_size,
        )

        test_results += run_tests(
            use_fp16=use_fp16,
            use_merged_qkv_weights=False,
            use_half4=True,
            batch_size=batch_size,
        )

    test_results += run_tests(
        use_fp16=use_fp16,
        use_merged_qkv_weights=False,
        use_half4=False,
        batch_size=batch_size,
    )

    return test_results

