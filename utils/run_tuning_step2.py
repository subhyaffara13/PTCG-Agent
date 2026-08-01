
def run_tuning_step2(task, mixed_precision_baseline, optimized_ops):
    """Assumed that you have run step 0 and 1 to figure out that Logits FP32 and some operators shall be in FP32,
    This step will try add one more operator.
    """
    candidate_fp32_ops = ["FastGelu", "LayerNormalization", "SkipLayerNormalization"]
    fp32_ops = [x for x in candidate_fp32_ops if x in optimized_ops]
    for op in optimized_ops:
        if op not in fp32_ops:
            op_block_list = [*fp32_ops, op]
            task.run(
                [*mixed_precision_baseline, "--op_block_list", *op_block_list],
                "Mixed precision baseline + {},{} in FP32".format(",".join(fp32_ops), op),
            )

