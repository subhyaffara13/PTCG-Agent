
def run_one_test(model_setting, test_setting, perf_results, all_inputs, intra_op_num_threads):
    session = create_session(
        model_setting.model_path,
        test_setting.use_gpu,
        test_setting.provider,
        intra_op_num_threads,
        model_setting.opt_level,
        log_severity=test_setting.log_severity,
        tuning_results_path=model_setting.input_tuning_results,
    )
    output_names = [output.name for output in session.get_outputs()]

    key = to_string(model_setting.model_path, session, test_setting)
    if key in perf_results:
        print("skip duplicated test:", key)
        return

    print("Running test:", key)

    all_latency_list = []
    if test_setting.use_io_binding:
        for _i in range(test_setting.test_times):
            results, latency_list = onnxruntime_inference_with_io_binding(
                session, all_inputs, output_names, test_setting
            )
            all_latency_list.extend(latency_list)
    else:
        for _i in range(test_setting.test_times):
            results, latency_list = onnxruntime_inference(session, all_inputs, output_names)
            all_latency_list.extend(latency_list)

    # latency in milliseconds
    latency_ms = np.array(all_latency_list) * 1000

    average_latency = statistics.mean(latency_ms)
    latency_50 = np.percentile(latency_ms, 50)
    latency_75 = np.percentile(latency_ms, 75)
    latency_90 = np.percentile(latency_ms, 90)
    latency_95 = np.percentile(latency_ms, 95)
    latency_99 = np.percentile(latency_ms, 99)
    throughput = test_setting.batch_size * (1000.0 / average_latency)

    perf_results[key] = (
        average_latency,
        latency_50,
        latency_75,
        latency_90,
        latency_95,
        latency_99,
        throughput,
    )

    print(
        "Average latency = {} ms, Throughput = {} QPS".format(format(average_latency, ".2f"), format(throughput, ".2f"))
    )

    if model_setting.output_tuning_results:
        output_path = os.path.abspath(model_setting.output_tuning_results)
        if os.path.exists(output_path):
            old_output_path = output_path
            output_path = f"""{output_path.rsplit(".json", 1)[0]}.{datetime.now().timestamp()}.json"""
            print("WARNING:", old_output_path, "exists, will write to", output_path, "instead.")

        trs = session.get_tuning_results()
        with open(output_path, "w") as f:
            json.dump(trs, f)
        print("Tuning results is saved to", output_path)

