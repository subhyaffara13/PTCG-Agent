import json
from typing import Any

def action_step(args: Any) -> Any:
    env = {"logs": args.logs}
    try:
        env = make(args.environment, args.configuration, args.info, args.steps, args.logs, args.debug)
        runner = env.__agent_runner(args.agents)
        env.step(runner.act())
    finally:
        if args.log_path is not None:
            with open(args.log_path, mode="a") as log_file:
                json.dump(env.logs[-1], log_file)
                log_file.write(",")
    return render(args, env)

