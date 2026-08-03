from typing import Any

def test_ort_latency(
    device,
    model,
    model_name,
    description,
    ort_session,
    batch_sizes,
    sequence_lengths,
    global_lengths,
    test_times,
    num_threads,
    optimizer=False,
    precision="fp32",
    disable_io_binding=False,
    verbose=True,
    use_compact_memory=False,
    use_half4=False,
    disable_parity=False,
) -> list[dict[str, Any]]:
    results = []
    for batch_size in batch_sizes:
        for sequence_length in sequence_lengths:
            for global_length in global_lengths:
                assert global_length <= model.config.attention_window[0], (
                    "Limitation of current implementation: number of global token <= attention_window"
                )

                logger.info(
                    f"Testing batch_size={batch_size} sequence_length={sequence_length} global_length={global_length} "
                    f"optimizer={optimizer}, precision={precision} io_binding={not disable_io_binding}..."
                )
                dummy_inputs: LongformerInputs = LongformerHelper.get_dummy_inputs(
                    batch_size, sequence_length, global_length, device
                )

                # Run OnnxRuntime
                ort_inputs = dummy_inputs.get_ort_inputs()

                if verbose:
                    print(ort_inputs)

                # run one query for warm up
                ort_outputs = ort_session.run(None, ort_inputs)

                result_template = {
                    "model_name": model_name,
                    "description": description,
                    "inputs": 3,
                    "engine": "OnnxRuntime",
                    "version": str(onnxruntime.__version__),
                    "device": "cuda",
                    "precision": str(precision),
                    "optimizer": int(optimizer),
                    "threads": int(num_threads),
                    "batch_size": int(batch_size),
                    "sequence_length": int(sequence_length),
                    "global_length": int(global_length),
                    "test_times": int(test_times),
                    "datetime": str(datetime.now()),
                    "memory": "",
                    "diff_max": None,
                    "diff_90_percentile": None,
                    "diff_95_percentile": None,
                    "diff_99_percentile": None,
                    "use_compact_memory": use_compact_memory,
                    "use_half4": use_half4,
                }

                if not disable_io_binding:
                    max_last_state_size = max(batch_sizes) * max(sequence_lengths) * model.config.hidden_size
                    max_pooler_size = max(batch_sizes) * max(sequence_lengths)
                    result = benchmark_helper.inference_ort_with_io_binding(
                        ort_session,
                        ort_inputs,
                        result_template=result_template,
                        repeat_times=test_times,
                        ort_output_names=["last_state", "pooler"],
                        ort_outputs=ort_outputs,
                        output_buffers=[],
                        output_buffer_max_sizes=[max_last_state_size, max_pooler_size],
                        batch_size=batch_size,
                        device=device,
                        data_type=np.longlong,  # input data type
                    )
                else:
                    result = benchmark_helper.inference_ort(
                        ort_session,
                        ort_inputs,
                        result_template=result_template,
                        repeat_times=test_times,
                        batch_size=batch_size,
                    )

                # measure result difference between PyTorch and OnnxRuntime
                if not disable_parity:
                    diff_results = [
                        test_parity(
                            device,
                            model,
                            ort_session,
                            batch_size,
                            sequence_length,
                            global_length,
                            verbose,
                        )
                        for _ in range(test_times)
                    ]

                    result["diff_max"] = max(diff_results)
                    result["diff_90_percentile"] = np.percentile(diff_results, 90)
                    result["diff_95_percentile"] = np.percentile(diff_results, 95)
                    result["diff_99_percentile"] = np.percentile(diff_results, 99)

                results.append(result)
    return results

