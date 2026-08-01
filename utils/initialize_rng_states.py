
def initialize_rng_states(
    num_rng: int,
    graphsafe_idx: int,
    fwd_rng_states: list[torch.Generator],
    bwd_rng_states: list[torch.Generator],
) -> None:
    """
    Initialize the cudagraph safe rng states.

    Initialization of rng states should have a few properties:
    - the initialization for each rng state should be independent
    - the initialization should be deterministic
    - the initialization should be based off current rng state, so that independent graphs do not
    have equal rng behavior

    We defer initialization of rng states until runtime because compilation is wrapped
    with preserve_rng_states. Seed initialization should advance the rng states so consecutive compilations
    do not give equal randomness.
    """
    with torch.utils._python_dispatch._disable_current_modes():
        seeds = torch.randint(0, torch.iinfo(torch.int64).max, (num_rng,), device="cpu")
        fwd_rng_states.extend(
            [
                torch.cuda.default_generators[graphsafe_idx]
                .clone_state()
                .manual_seed(int(seeds[i]))
                for i in range(num_rng)
            ]
        )
        bwd_rng_states.extend(
            [
                torch.cuda.default_generators[graphsafe_idx]
                .clone_state()
                .manual_seed(int(seeds[i]))
                for i in range(num_rng)
            ]
        )

