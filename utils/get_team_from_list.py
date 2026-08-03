from typing import List, Optional, Union

def get_team_from_list(
    team_list: Optional[Union[List[LiteLLM_TeamTable], List[TeamListResponseObject]]],
    team_id: str,
) -> Optional[Union[LiteLLM_TeamTable, LiteLLM_TeamMembership]]:
    if team_list is None:
        return None

    for team in team_list:
        if team.team_id == team_id:
            return team
    return None

