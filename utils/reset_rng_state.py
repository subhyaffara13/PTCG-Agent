
def reset_rng_state(use_xla: bool = False) -> None:
    torch.manual_seed(1337)
    random.seed(1337)
    if np:
        np.random.seed(1337)
    if use_xla:
        import torch_xla.core.xla_model as xm

        xm.set_rng_state(1337, str(xm.xla_device()))

