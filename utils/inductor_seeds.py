
def inductor_seeds(count, device):
    warn_triton_random()
    return TensorBox.create(ir.RandomSeeds(count, decode_device(device)))

