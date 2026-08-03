from typing import Dict, List, Optional, Union

def _convert_teams_to_response_models(
    teams: list,
    use_deleted_table: bool,
    keys_count_by_team: Optional[Dict[str, int]] = None,
) -> List[Union[TeamListItem, LiteLLM_TeamTable, LiteLLM_DeletedTeamTable]]:
    """Convert raw Prisma team rows to response models."""
    team_list: List[
        Union[TeamListItem, LiteLLM_TeamTable, LiteLLM_DeletedTeamTable]
    ] = []
    counts = keys_count_by_team or {}
    for team in teams:
        try:
            team_dict = team.model_dump()
        except Exception:
            team_dict = team.dict()

        if use_deleted_table:
            team_list.append(LiteLLM_DeletedTeamTable(**team_dict))
        else:
            members_with_roles = team_dict.get("members_with_roles")
            if not isinstance(members_with_roles, list):
                members_with_roles = []
                team_dict["members_with_roles"] = members_with_roles
            members_count = len(members_with_roles)
            keys_count = counts.get(team_dict.get("team_id") or "", 0)
            team_list.append(
                TeamListItem(
                    **team_dict,
                    members_count=members_count,
                    keys_count=keys_count,
                )
            )
    return team_list

