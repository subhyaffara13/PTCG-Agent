from typing import Any

def launch_test(model_setting, test_setting, perf_results, all_inputs, intra_op_num_threads):
    process = multiprocessing.Process(
        target=run_one_test,
        args=(
            model_setting,
            test_setting,
            perf_results,
            all_inputs,
            intra_op_num_threads,
        ),
    )
    process.start()
    process.join()


def launch_test(arguments) -> list[dict[str, Any]]:
    if not torch.cuda.is_available():
        raise RuntimeError("Please install PyTorch with Cuda, and use a machine with GPU for testing gpu performance.")

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run, [arguments]))
        assert len(results) == 1
        return results[0]

