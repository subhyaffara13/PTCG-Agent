from typing import Callable, Dict, List

def human_readable_agent(agent: Callable[[Dict], Action]):
    """
    Decorator allowing for more human-friendly implementation of the agent function.

    @human_readable_agent
    def my_agent(obs):
        ...
        return football_action_set.action_right
    """

    @wraps(agent)
    def agent_wrapper(obs) -> List[int]:
        # Extract observations for the first (and only) player we control.
        obs = obs["players_raw"][0]
        # Turn 'sticky_actions' into a set of active actions (strongly typed).
        obs["sticky_actions"] = {
            sticky_index_to_action[nr] for nr, action in enumerate(obs["sticky_actions"]) if action
        }
        # Turn 'game_mode' into an enum.
        obs["game_mode"] = GameMode(obs["game_mode"])
        # In case of single agent mode, 'designated' is always equal to 'active'.
        if "designated" in obs:
            del obs["designated"]
        # Conver players' roles to enum.
        obs["left_team_roles"] = [PlayerRole(role) for role in obs["left_team_roles"]]
        obs["right_team_roles"] = [PlayerRole(role) for role in obs["right_team_roles"]]

        action = agent(obs)
        return [action.value]

    return agent_wrapper

