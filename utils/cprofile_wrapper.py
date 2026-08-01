
def cprofile_wrapper(func: Callable[_P, _T]) -> Callable[_P, _T]:
    @functools.wraps(func)
    def profile_wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        trace_id = CompileContext.current_trace_id()
        assert trace_id, "Trace id is None"
        profile_path = Path(
            os.path.join(
                tempfile.gettempdir(),
                f"{func.__name__}_{str(trace_id).replace('/', '_')}.profile",
            )
        )
        prof = cProfile.Profile()
        try:
            start_ts = time.time()
            # runcall calls prof.enable() and prof.disable(), so do NOT call
            # enable outside. This leads to issues like
            # ValueError: Another profiling tool is already active
            # pyrefly: ignore [bad-argument-type]
            retval = prof.runcall(func, *args, **kwargs)
            profile_latency = time.time() - start_ts
        except ValueError:
            log.exception("failed to enable cProfile")
            profile_latency = 0
            retval = func(*args, **kwargs)
        log.warning(
            "### Cprofile for %s trace id [%s] took %.3f seconds ###",
            func.__name__,
            trace_id,
            profile_latency,
        )
        ps = pstats.Stats(prof)
        try:
            prof.dump_stats(profile_path)
        except OSError:
            log.exception("Cannot write to %s", profile_path)
        log.warning("Raw profile at %s", profile_path)
        svg_path = profile_path.with_suffix(".svg")
        try:
            with subprocess.Popen(
                [
                    "gprof2dot",
                    "-f",
                    "pstats",
                    "--node-label=total-time-percentage",
                    "--node-label=self-time-percentage",
                    "--node-label=total-time",
                    str(profile_path),
                ],
                stdout=subprocess.PIPE,
            ) as gprof2dot_process:
                subprocess.check_call(
                    ["dot", "-Tsvg", "-o", str(svg_path)],
                    stdin=gprof2dot_process.stdout,
                )
                log.warning("Generated SVG from profile at %s", svg_path)
        except FileNotFoundError:
            log.warning(
                "Failed to generate SVG from profile -- dumping stats instead."
                "Try installing gprof2dot and dot for a better visualization"
            )
            ps.sort_stats(pstats.SortKey.TIME).print_stats(20)
            ps.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)

        if manifold_link := maybe_upload_prof_stats_to_manifold(
            str(profile_path)
        ):  # fb-only
            torch._logging.trace_structured(
                "link",
                lambda: {"name": "cprofile_manifold_url", "url": manifold_link},
            )
        return retval

    return profile_wrapper

