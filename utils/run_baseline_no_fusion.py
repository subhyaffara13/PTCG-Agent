
def run_baseline_no_fusion(ir, inputs) -> float:
    with no_fuser():
        return run_test(ir, inputs)

