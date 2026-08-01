
def _create_autograd_profiler():
    return torch.autograd.profiler.profile(record_shapes=True)

