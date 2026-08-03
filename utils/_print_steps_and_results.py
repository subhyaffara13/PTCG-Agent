from typing import Any

def _print_steps_and_results(env: Any) -> None:
    print("\n=== GAME STEPS ===")
    for idx, step in enumerate(env.steps):
        print(f"--- Step {idx} ---")
        for agent_idx, agent_state in enumerate(step):
            print(f"  Agent {agent_idx} ({agent_state.status}): {agent_state.action}")

    print("\n=== RESULTS ===")
    for i, state in enumerate(env.state):
        print(f"Agent {i}: status={state.status}, reward={state.reward}")

