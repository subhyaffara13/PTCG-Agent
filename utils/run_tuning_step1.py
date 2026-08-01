
def run_tuning_step1(task, mixed_precision_baseline, optimized_ops):
    """Step 1 is to figure out which optimized operator in FP32 could benefit most"""
    for op in optimized_ops:
        op_block_list = ["--op_block_list", op]
        task.run(
            mixed_precision_baseline + op_block_list,
            f"Mixed precision baseline + {op} in FP32",
        )

