
def get_team_roles(base_roles: List[str]) -> (List[str], List[str]):
    """Partitions roles into villager and werewolf teams."""
    villager_roles = []
    werewolf_roles = []
    for role_name in base_roles:
        role = RoleConst(role_name)
        if role == RoleConst.WEREWOLF:
            werewolf_roles.append(role_name)
        else:
            villager_roles.append(role_name)
    return villager_roles, werewolf_roles

