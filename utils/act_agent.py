from typing import Any

def act_agent(args: tuple[Agent | None, dict[str, Any], dict[str, Any], Any]) -> tuple[Any, dict[str, Any]]:
    agent, state, configuration, none_action = args
    if state["status"] != "ACTIVE":
        return None, {}
    elif agent is None:
        return none_action, {}
    else:
        return agent.act(state["observation"])

