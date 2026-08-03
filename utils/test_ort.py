import os
from typing import Any

def test_ort(args, device) -> list[dict[str, Any]]:
    model_name = args.model

    onnx_model_path = find_onnx_model(model_name) if not args.onnx else args.onnx

    optimized = onnx_model_path.endswith("_fp16.onnx") or onnx_model_path.endswith("_fp32.onnx")  # noqa: PIE810
    precision = "fp32" if not onnx_model_path.endswith("_fp16.onnx") else "fp16"

    model = load_torch_model(model_name, device)

    num_threads = args.num_threads

    cuda_provider_options = {"arena_extend_strategy": "kSameAsRequested"}
    provider_options = {"CUDAExecutionProvider": cuda_provider_options}
    session = benchmark_helper.create_onnxruntime_session(
        onnx_model_path,
        use_gpu=True,
        enable_all_optimization=True,
        num_threads=num_threads,
        provider_options=provider_options,
    )
    if session is None:
        raise RuntimeError(f"Failed to create ORT session from ONNX file {onnx_model_path}")

    use_compact_memory = os.environ.get("ORT_LONGFORMER_COMPACT_MEMORY", "1") == "1"
    description = onnx_model_path
    if not use_compact_memory:
        description += "[non_compact_memory]"

    if args.use_half4:
        description += "[half4]" if precision == "fp16" else "[float4]"
    else:
        description += "[half2]" if precision == "fp16" else "[float4]"

    return test_ort_latency(
        device,
        model,
        model_name,
        description,
        session,
        args.batch_sizes,
        args.sequence_lengths,
        args.global_lengths,
        args.test_times,
        num_threads,
        optimized,
        precision,
        args.disable_io_binding,
        args.verbose,
        use_compact_memory,
        args.use_half4,
        args.disable_parity,
    )

