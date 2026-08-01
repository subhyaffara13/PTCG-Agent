
def run_tuning_step0(task, fp16_baseline, all_ops, optimized_ops):
    """Step 0 is to check which operator in FP16 causes most loss"""
    fp32_logits = ["--io_block_list", "logits"]
    task.run(fp16_baseline + fp32_logits, "FP16 except logits")

    fp32_io = ["--keep_io_types"]
    task.run(fp16_baseline + fp32_io, "Graph I/O FP32, Other FP16")

    # Only weights in FP16
    task.run(
        fp16_baseline + fp32_io + ["--op_block_list"] + list(all_ops) + ["--force_fp16_initializers"],
        "FP32 except weights in FP16",
    )

    optimized_ops_results = []
    op_list = optimized_ops
    for op in op_list:
        op_block_list = ["--op_block_list"] + [o for o in op_list if o != op]
        result = task.run(fp16_baseline + fp32_io + op_block_list, f"FP32 except {op} in FP16")
        if result:
            optimized_ops_results.append(result)

    # Check which optimized operator causes the most loss in precision
    min_result = min(optimized_ops_results, key=lambda y: y["top1_match_rate"])
    print("step 0: optimized operator causes the most loss in precision", min_result)

