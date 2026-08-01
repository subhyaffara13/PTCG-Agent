
def should_prefer_unfused_addmm(match):
    inp = match.kwargs["inp"]
    if not is_gpu(inp.meta["val"].device.type):
        return False

    output = match.output_node()
    return all(is_pointwise_use(use) for use in output.users)

