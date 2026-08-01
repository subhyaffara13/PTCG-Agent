
def agent_launch_args(command: str, base_url: str) -> List[str]:
    """Extra CLI args an agent needs to actually honor the proxy.

    Claude Code and OpenCode respect the exported env vars, so they get nothing
    here; Codex needs its provider pointed via config overrides.
    """
    builder = _PROXY_ARGS.get(os.path.basename(command))
    return builder(base_url) if builder else []

