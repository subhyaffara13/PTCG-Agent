
def run_llm_game(
    env_name: str,
    *,
    caller_file: str,
    agent_module: str = "harness.py",
    num_agents: int = 2,
    configuration: dict[str, Any] | None = None,
    replay_filename: str = "test-replay.json",
    cli: bool = True,
    argv: list[str] | None = None,
) -> Any:
    """Run a full game with LLM agents and save the replay.

    Args:
        env_name: Env to instantiate (e.g. ``"open_spiel_checkers"``).
        caller_file: Pass ``__file__`` from the caller. The helper resolves
            the agent path and the replay directory relative to this.
        agent_module: Path to the harness module relative to the caller's
            directory. Defaults to ``"harness.py"``; use ``"harness/main.py"``
            for packaged harnesses like word_association.
        num_agents: How many copies of the agent to pass to ``env.run``.
            Defaults to 2; word_association uses 4.
        configuration: Optional dict forwarded to ``make(configuration=...)``.
        replay_filename: Filename for the saved replay; written to
            ``<caller_dir>/visualizer/default/replays/<filename>`` by default.
        cli: When True (default), parse ``--model`` and ``--replay-path`` from
            ``sys.argv``. Set False to disable so the caller can bring its own
            argparse.
        argv: Optional override for ``sys.argv[1:]`` (test seam).

    Returns:
        The ``env`` after the run, so callers can do game-specific
        post-processing (e.g. word_association's winner banner).
        Returns ``None`` and prints a hint if no API key is present.
    """
    if not _check_api_keys():
        return None

    args = _parse_cli(argv if argv is not None else sys.argv[1:]) if cli else _parse_cli([])
    _set_env_defaults(args.model)

    env = make(env_name, configuration=configuration, debug=True)

    caller_dir = os.path.dirname(os.path.abspath(caller_file))
    agent_path = os.path.join(caller_dir, agent_module)
    replay_path = args.replay_path or os.path.join(
        caller_dir, _REPLAY_SUBDIR, replay_filename,
    )

    print(f"Running {env_name} with LLM agents (model={os.environ['MODEL_NAME']})...")
    env.run([agent_path] * num_agents)

    _print_steps_and_results(env)
    _save_replay(env, replay_path)

    return env

