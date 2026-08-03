import os
from typing import Any, Callable, Dict, Tuple

def build_agent(
    raw: str | Callable | Any, builtin_agents: Dict[str, Callable], environment_name: str
) -> Tuple[Callable, bool]:
    """
    Returns the agent and whether the agent is parallelizable.
    """
    if isinstance(raw, str) and raw in builtin_agents:
        agent = builtin_agents[raw]
        # TODO: Below is a hack. Assuming an agent is a global callable is not enough to guarantee it is stateless.
        #  Kaggle environment should allow more scalable agent initialization and proper agent interface design.
        if hasattr(agent, "reset") and callable(getattr(agent, "reset", None)):
            agent.reset()  # type: ignore[attr-defined]
        return builtin_agents[raw], False

    # Already callable.
    if callable(raw):
        return raw, False

    # Not a string, static action.
    if not isinstance(raw, str):
        return lambda: raw, False

    # A URL and will be initialized on the calling server.
    if is_url(raw):
        return UrlAgent(raw, environment_name), True

    # A path exists and attempt to grab the source (fallback to the original string).
    raw_agent = raw
    if os.path.exists(raw):
        raw_agent = read_file(raw, raw)
    elif (len(raw) < 100 and ("/" in raw or "\\" in raw)) or len(raw) < 20:
        raise FileNotFoundError("Could not find : " + raw)

    # Attempt to execute the last callable or just return the string.
    agent = None

    def callable_agent(observation: Any, configuration: Any) -> Any:
        nonlocal agent
        if agent is None:
            agent = get_last_callable(raw_agent, path=raw) or raw_agent
        configuration["__raw_path__"] = raw
        args = [observation, configuration]
        if hasattr(agent, "__code__") and hasattr(agent.__code__, "co_argcount"):
            args = args[: agent.__code__.co_argcount]
        return agent(*args) if callable(agent) else agent

    return callable_agent, False

