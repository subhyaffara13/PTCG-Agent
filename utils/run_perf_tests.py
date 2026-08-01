
def run_perf_tests(model_setting, test_setting, perf_results, all_inputs):
    if test_setting.intra_op_num_threads is not None:
        launch_test(
            model_setting,
            test_setting,
            perf_results,
            all_inputs,
            test_setting.intra_op_num_threads,
        )
        return

    cpu_count = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)

    candidate_threads = list({logical_cores, cpu_count})
    for i in range(1, min(16, logical_cores)):
        if i not in candidate_threads:
            candidate_threads.append(i)
    candidate_threads.sort(reverse=True)

    for intra_op_num_threads in candidate_threads:
        launch_test(model_setting, test_setting, perf_results, all_inputs, intra_op_num_threads)

