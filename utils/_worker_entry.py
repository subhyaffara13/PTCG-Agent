
def _worker_entry(args: tuple) -> GameResult:
    """Picklable worker entrypoint for ProcessPoolExecutor.map / submit.

    Wraps :func:`run_one_game` in a SIGALRM watchdog so a single stuck LLM
    call doesn't block the worker process forever (the staging proxy is
    known to drop connections mid-stream, and litellm's retry loop can
    spin indefinitely). On timeout the worker returns a crash result and
    is free to take the next cell.
    """
    env_name, cell, variant_obj, api_key, api_base, timeout_secs, status_dir = args
    start = time.perf_counter()
    started_at = time.time()
    _write_status(status_dir or "", cell, "starting", started_at,
                  moves_p0=0, moves_p1=0)
    if timeout_secs and timeout_secs > 0:
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(int(timeout_secs))
    try:
        return run_one_game(
            env_name, cell, variant_obj, api_key, api_base,
            status_dir=status_dir, started_at=started_at,
        )
    except _AblationTimeout:
        return GameResult(
            variant=cell.variant, model_p0=cell.model_p0, model_p1=cell.model_p1,
            pair_role=cell.pair_role, seed=cell.seed,
            score_p0=0.0, score_p1=0.0, winner=0, length_moves=0,
            crash_p0=True, crash_p1=True,
            error=f"TimeoutError: exceeded {timeout_secs}s",
            duration_s=time.perf_counter() - start,
        )
    except Exception as exc:  # noqa: BLE001
        return GameResult(
            variant=cell.variant, model_p0=cell.model_p0, model_p1=cell.model_p1,
            pair_role=cell.pair_role, seed=cell.seed,
            score_p0=0.0, score_p1=0.0, winner=0, length_moves=0,
            crash_p0=True, crash_p1=True,
            error=f"{type(exc).__name__}: {exc}",
            duration_s=time.perf_counter() - start,
        )
    finally:
        if timeout_secs and timeout_secs > 0:
            signal.alarm(0)
        _clear_status(status_dir or "", cell)

