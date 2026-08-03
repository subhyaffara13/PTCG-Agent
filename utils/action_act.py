import json
from typing import Any

def action_act(args: Any) -> dict[str, Any]:
    global cached_agent
    if len(args.agents) != 1:
        return {"error": "One agent must be provided."}
    raw = args.agents[0]

    env = make(args.environment, args.configuration, args.info, state=args.state, debug=args.debug)

    is_first_run = cached_agent is None or cached_agent.raw != raw
    if is_first_run:
        cached_agent = Agent(raw, env)

    assert cached_agent is not None
    observation = utils.get(args.state, dict, {}, ["observation"])
    action, log = cached_agent.act(observation)
    if isinstance(action, errors.DeadlineExceeded):
        action = "DeadlineExceeded"
    elif isinstance(action, BaseException):
        action = "BaseException::" + str(action)

    if args.log_path is not None:
        with open(args.log_path, mode="a") as log_file:
            if not is_first_run:
                log_file.write(",\n ")
            json.dump([log], log_file)

    return {"action": action}

