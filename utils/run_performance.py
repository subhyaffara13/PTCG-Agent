
def run_performance(model_setting, test_setting, perf_results):
    input_ids, segment_ids, input_mask = get_bert_inputs(
        model_setting.model_path,
        model_setting.input_ids_name,
        model_setting.segment_ids_name,
        model_setting.input_mask_name,
    )

    # Do not generate random mask for performance test.
    print(
        f"Generating {test_setting.test_cases} samples for batch_size={test_setting.batch_size} sequence_length={test_setting.sequence_length}"
    )
    all_inputs = generate_test_data(
        test_setting.batch_size,
        test_setting.sequence_length,
        test_setting.test_cases,
        test_setting.seed,
        test_setting.verbose,
        input_ids,
        segment_ids,
        input_mask,
        test_setting.average_sequence_length,
        test_setting.random_sequence_length,
        mask_type=model_setting.mask_type,
    )

    run_perf_tests(model_setting, test_setting, perf_results, all_inputs)

