from typing import Any

def test_torch_latency(
    device,
    model,
    model_name,
    batch_sizes,
    sequence_lengths,
    global_lengths,
    test_times,
    num_threads,
) -> list[dict[str, Any]]:
    if num_threads > 0:
        torch.set_num_threads(num_threads)

    results = []
    for batch_size in batch_sizes:
        for sequence_length in sequence_lengths:
            for global_length in global_lengths:
                logger.info(f"batch_size={batch_size} sequence_length={sequence_length} global_length={global_length}")
                inputs: LongformerInputs = LongformerHelper.get_dummy_inputs(
                    batch_size, sequence_length, global_length, device
                )
                input_list = inputs.to_list()

                _ = model(*input_list)
                runtimes = timeit.repeat(lambda: model(*input_list), repeat=test_times, number=1)  # noqa: B023
                result = {
                    "engine": "torch",  # TODO: test torchscript
                    "version": torch.__version__,
                    "device": "cuda",
                    "optimizer": "",
                    "precision": "fp32",
                    "io_binding": "",
                    "model_name": model_name,
                    "description": model_name + " [torch]",
                    "inputs": 3,
                    "threads": num_threads,
                    "batch_size": batch_size,
                    "sequence_length": sequence_length,
                    "global_length": global_length,
                    "datetime": str(datetime.now()),
                    "memory": "NA",
                    "diff_max": 0,
                    "diff_90_percentile": 0,
                    "diff_95_percentile": 0,
                    "diff_99_percentile": 0,
                    "use_compact_memory": "NA",
                }
                result.update(benchmark_helper.get_latency_result(runtimes, batch_size))
                logger.info("%s", result)
                results.append(result)
    return results

