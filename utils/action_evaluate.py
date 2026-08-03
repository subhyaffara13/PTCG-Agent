import json
from typing import Any

def action_evaluate(args: Any) -> str:
    return json.dumps(evaluate(args.environment, args.agents, args.configuration, args.steps, args.episodes))

