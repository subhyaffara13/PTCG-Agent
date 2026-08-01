
def preserve_rng_state() -> Generator[None, None, None]:
    disable_functorch = torch._C._DisableFuncTorch
    disable_current_modes = torch.utils._python_dispatch._disable_current_modes
    with disable_current_modes(), disable_functorch():
        rng_state = torch.clone(torch.random.get_rng_state())
        skip_frame_if_in_functorch_mode(rng_state)
        if torch.cuda.is_available():
            cuda_rng_state = torch.clone(torch.cuda.get_rng_state())
        if torch.xpu.is_available():
            xpu_rng_state = torch.clone(torch.xpu.get_rng_state())
    try:
        yield
    finally:
        with torch.utils._python_dispatch._disable_current_modes():
            torch.random.set_rng_state(rng_state)
            if torch.cuda.is_available():
                torch.cuda.set_rng_state(cuda_rng_state)  # type: ignore[possibly-undefined]
            if torch.xpu.is_available():
                torch.xpu.set_rng_state(xpu_rng_state)  # type: ignore[possibly-undefined]

