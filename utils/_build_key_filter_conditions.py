from typing import Any, Dict, List, Optional, Union

def _build_key_filter_conditions(
    user_id: Optional[str],
    team_id: Optional[str],
    organization_id: Optional[str],
    key_alias: Optional[str],
    key_hash: Optional[str],
    exclude_team_id: Optional[str],
    admin_team_ids: Optional[List[str]],
    member_team_ids: Optional[List[str]] = None,
    include_created_by_keys: bool = False,
    project_id: Optional[str] = None,
    access_group_id: Optional[str] = None,
    use_substring_matching: bool = False,
) -> Dict[str, Union[str, Dict[str, Any], List[Dict[str, Any]]]]:
    """Build filter conditions for key listing.

    Visibility rules:
    - Users always see their own keys (user_id match)
    - Team admins see ALL keys for their admin teams (via admin_team_ids)
    - Regular team members see only service accounts (user_id=NULL) for their
      teams (via member_team_ids). This prevents leaking other members' spend data.
    - created_by visibility is scoped to teams the user currently belongs to,
      so former members cannot see service accounts they created after leaving.
    """
    # Prepare filter conditions
    where: Dict[str, Union[str, Dict[str, Any], List[Dict[str, Any]]]] = {}
    where.update(_get_condition_to_filter_out_ui_session_tokens())

    # Build the OR conditions for user's keys and admin team keys
    or_conditions: List[Dict[str, Any]] = []

    # Base conditions for user's own keys
    user_condition: Dict[str, Any] = {}
    if user_id and isinstance(user_id, str):
        if use_substring_matching:
            user_condition["user_id"] = {
                "contains": user_id,
                "mode": "insensitive",
            }
        else:
            user_condition["user_id"] = user_id
    if key_alias and isinstance(key_alias, str):
        if use_substring_matching:
            user_condition["key_alias"] = {
                "contains": key_alias,
                "mode": "insensitive",
            }
        else:
            user_condition["key_alias"] = key_alias
    if exclude_team_id and isinstance(exclude_team_id, str):
        user_condition["team_id"] = {"not": exclude_team_id}
    if organization_id and isinstance(organization_id, str):
        user_condition["organization_id"] = organization_id
    if key_hash and isinstance(key_hash, str):
        user_condition["token"] = key_hash

    if user_condition:
        or_conditions.append(user_condition)

    # Add condition for created_by keys, scoped to user's current teams
    if include_created_by_keys and user_id:
        if member_team_ids is not None:
            if member_team_ids:
                # Scope created_by keys to teams user is still a member of,
                # or keys that have no team (personal keys)
                or_conditions.append(
                    {
                        "AND": [
                            {"created_by": user_id},
                            {
                                "OR": [
                                    {"team_id": {"in": member_team_ids}},
                                    {"team_id": None},
                                ]
                            },
                        ]
                    }
                )
            else:
                # User is not a member of any team, only show non-team created_by keys
                or_conditions.append(
                    {"AND": [{"created_by": user_id}, {"team_id": None}]}
                )
        else:
            # No team membership info provided (backward compatibility for
            # direct _list_key_helper callers like Prometheus)
            or_conditions.append({"created_by": user_id})

    # Add condition for admin team keys (admins see ALL team keys)
    if admin_team_ids:
        or_conditions.append({"team_id": {"in": admin_team_ids}})

    # Add condition for member team service accounts (members only see keys with user_id=NULL)
    if member_team_ids:
        # Exclude teams where user is already admin (those are covered above with full visibility)
        member_only_team_ids = [
            tid for tid in member_team_ids if tid not in (admin_team_ids or [])
        ]
        if member_only_team_ids:
            or_conditions.append(
                {
                    "AND": [
                        {"team_id": {"in": member_only_team_ids}},
                        {"user_id": None},
                    ]
                }
            )

    # Combine conditions with OR if we have multiple conditions
    if len(or_conditions) > 1:
        where = {"AND": [where, {"OR": or_conditions}]}
    elif len(or_conditions) == 1:
        where.update(or_conditions[0])

    # Apply team_id, project_id and access_group_id as global AND filters so they
    # narrow results across all visibility conditions (own keys, team keys, etc.)
    if team_id and isinstance(team_id, str):
        where = {"AND": [where, {"team_id": team_id}]}
    if project_id:
        where = {"AND": [where, {"project_id": project_id}]}
    if access_group_id:
        where = {"AND": [where, {"access_group_ids": {"hasSome": [access_group_id]}}]}

    verbose_proxy_logger.debug(f"Filter conditions: {where}")
    return where

