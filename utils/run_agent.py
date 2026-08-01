
def run_agent(agent, n_steps):
    while True:
        agent.run_episode(n_steps=n_steps)
        agent.finish_episode()

        if agent.running_reward > agent.reward_threshold:
            print(f"Solved! Running reward is now {agent.running_reward}!")
            break


def run_agent(
    base_url: str,
    api_key: str,
    command: Sequence[str],
    *,
    skip_verify: bool = False,
    base_env: Optional[Mapping[str, str]] = None,
    which: Callable[[str], Optional[str]] = shutil.which,
    verify: Callable[[str, str], None] = verify_proxy_key,
    launcher: Callable[[str, Sequence[str], Mapping[str, str]], None] = _exec,
    reattach_terminal: Optional[Callable[[], None]] = None,
) -> None:
    """Validate, wire the environment, and hand off to the agent.

    On success this replaces the current process and never returns. Raises
    AgentRunError for missing binaries, an unreachable proxy, or a rejected key.
    reattach_terminal, when given, runs just before handoff to restore stdin.
    """
    if not command:
        raise AgentRunError("Nothing to run.")

    _, profiles = agent_profile(command[0])
    binary = which(command[0])
    if binary is None:
        docs = _INSTALL_DOCS.get(os.path.basename(command[0]))
        hint = f" Install it first: {docs}" if docs else ""
        raise AgentRunError(f"Could not find `{command[0]}` on your PATH.{hint}")

    if not skip_verify:
        verify(base_url, api_key)

    env = build_agent_env(
        base_env if base_env is not None else os.environ,
        base_url,
        api_key,
        profiles,
    )
    extra_args = agent_launch_args(command[0], base_url)
    if reattach_terminal is not None:
        reattach_terminal()
    launcher(binary, [command[0], *extra_args, *command[1:]], env)

