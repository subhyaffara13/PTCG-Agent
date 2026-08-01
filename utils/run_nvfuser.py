
def run_nvfuser(ir, inputs) -> float:
    with torch.jit.fuser("fuser2"):
        return run_test(ir, inputs)

