
def run_one_game(
    env_name: str,
    cell: GameCell,
    variant_obj: GameHarness,
    api_key: str,
    api_base: str,
    *,
    configuration_extras: Mapping[str, Any] | None = None,
    status_dir: str | None = None,
    started_at: float | None = None,
) -> GameResult:
    """Play one cell to completion and return its row.

    Called in a worker process by :func:`cmd_run`. Safe to call directly
    for testing -- no shared state beyond what's passed in.

    If ``status_dir`` is provided, each agent invocation triggers a
    status-file write so the parent's monitor thread can show live
    per-game progress.
    """
    start = time.perf_counter()
    if started_at is None:
        started_at = time.time()
    config: dict[str, Any] = {"seed": int(cell.seed)}
    if configuration_extras:
        config.update(configuration_extras)
    error = ""

    # Per-seat move counters used by the status writer below.
    moves = [0, 0]

    def _wrap(seat: int, real_agent):
        def tracked(obs: Any, cfg: dict[str, Any]) -> dict[str, Any]:
            moves[seat] += 1
            _write_status(
                status_dir or "", cell, "running", started_at,
                moves_p0=moves[0], moves_p1=moves[1],
            )
            return real_agent(obs, cfg)
        return tracked

    agent_p0 = _wrap(0, create_agent_fn(
        variant_obj,
        model_override=build_model_setup(cell.model_p0, api_key, api_base),
    ))
    agent_p1 = _wrap(1, create_agent_fn(
        variant_obj,
        model_override=build_model_setup(cell.model_p1, api_key, api_base),
    ))

    env = make(env_name, configuration=config, debug=False)
    try:
        env.run([agent_p0, agent_p1])
        p0, p1, winner = _extract_scores(env)
        length = len(env.steps)
        crash_p0 = _agent_crashed(env, 0)
        crash_p1 = _agent_crashed(env, 1)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        _log.warning("Game crashed (%s): %s", cell, exc)
        p0 = p1 = 0.0
        winner = 0
        length = 0
        crash_p0 = crash_p1 = True

    return GameResult(
        variant=cell.variant,
        model_p0=cell.model_p0,
        model_p1=cell.model_p1,
        pair_role=cell.pair_role,
        seed=cell.seed,
        score_p0=p0,
        score_p1=p1,
        winner=winner,
        length_moves=length,
        crash_p0=crash_p0,
        crash_p1=crash_p1,
        error=error,
        duration_s=time.perf_counter() - start,
    )

