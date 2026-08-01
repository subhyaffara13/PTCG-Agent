
def checkpoint_params(gm: torch.fx.GraphModule) -> Callable[[], None]:
    with torch.no_grad():
        rng_state = torch.clone(torch.random.get_rng_state())
        if torch.cuda.is_available():
            cuda_rng_state = torch.clone(torch.cuda.get_rng_state())
        saved_state = [
            (param, param._version, torch.clone(param))
            # pyrefly: ignore [bad-argument-type]
            for param in itertools.chain(gm.parameters(), gm.buffers())
        ]

    def restore() -> None:
        with torch.no_grad():
            torch.random.set_rng_state(rng_state)
            if torch.cuda.is_available():
                torch.cuda.set_rng_state(cuda_rng_state)
            for param, version, original_value in saved_state:
                if param._version != version:
                    param.copy_(original_value)

    return restore

