
def run_parity(task: ParityTask, args):
    onnx_model_paths = Gpt2Helper.get_onnx_paths(
        "onnx_models",
        args.model_name_or_path,
        new_folder=args.use_external_data_format,
        remove_existing=[],
    )

    fp32_baseline, fp16_baseline = get_baselines(args)

    result = task.run(fp32_baseline, "FP32 baseline")

    optimized_ops = []
    if result and ("optimized_operators" in result) and result["optimized_operators"]:
        optimized_ops = result["optimized_operators"].split(",")
    else:
        raise RuntimeError("Failed to get optimized operators")

    all_ops = []
    if result and ("operators" in result) and result["operators"]:
        all_ops = result["operators"].split(",")
    else:
        raise RuntimeError("Failed to get operators")

    # The following tests for fp16 requires GPU
    if not args.use_gpu:
        logger.info("skip mixed precision since --use_gpu is not specified")
        return

    task.run(fp16_baseline, "FP16 baseline")

    last_matmul_node_name = get_last_matmul_node_name(onnx_model_paths["raw"])

    # Mixed precision baseline
    run_candidate(task, args, last_matmul_node_name, op_block_list=[])

    def get_fp32_ops(x):
        return [op for op in x if op in all_ops]

    if args.all:
        run_tuning_step0(task, fp16_baseline, all_ops, optimized_ops)
        mixed_precision_baseline = get_mixed_precision_parameters(args, last_matmul_node_name, op_block_list=[])
        run_tuning_step1(task, mixed_precision_baseline, optimized_ops)
        run_tuning_step2(task, mixed_precision_baseline, optimized_ops)
    else:
        run_candidate(
            task,
            args,
            last_matmul_node_name,
            op_block_list=get_fp32_ops(["SkipLayerNormalization", "LayerNormalization", "Add"]),
        )
        run_candidate(task, args, last_matmul_node_name, op_block_list=["FastGelu"])

    # Run a few good candidates
    run_candidate(
        task,
        args,
        last_matmul_node_name,
        op_block_list=get_fp32_ops(["FastGelu", "SkipLayerNormalization", "LayerNormalization", "Add"]),
    )
    run_candidate(
        task,
        args,
        last_matmul_node_name,
        op_block_list=get_fp32_ops(
            ["FastGelu", "EmbedLayerNormalization", "SkipLayerNormalization", "LayerNormalization", "Add"]
        ),
    )

