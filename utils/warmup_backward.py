
def warmup_backward(f, *args):
    profiling_count = 3
    results = []
    for _ in range(profiling_count):
        if len(args) > 0:
            r = torch.autograd.grad(f, *args)
            results.append(r)
        else:
            f.backward(retain_graph=True)

    return results

