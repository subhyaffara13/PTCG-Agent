from typing import List, Optional, Union

def check_if_default_team_set() -> Optional[Union[List[str], List[NewUserRequestTeam]]]:
    if litellm.default_internal_user_params is None:
        return None
    teams = litellm.default_internal_user_params.get("teams")
    if teams is not None:
        if all(isinstance(team, str) for team in teams):
            return teams
        elif all(isinstance(team, dict) for team in teams):
            return [
                NewUserRequestTeam(
                    team_id=team.get("team_id"),
                    max_budget_in_team=team.get("max_budget_in_team"),
                    user_role=team.get("user_role", "user"),
                )
                for team in teams
            ]
        else:
            verbose_proxy_logger.error(
                "Invalid team type in default internal user params: %s",
                teams,
            )
    return None

