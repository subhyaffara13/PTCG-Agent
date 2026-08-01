
def get_all_unique_role_configs(role_configs: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """
    Generates all unique permutations of role configurations.
    A role configuration is a dict with 'role' and 'role_params'.
    """

    def make_hashable(config):
        role = config["role"]
        params = config.get("role_params", {})
        if params:
            return role, frozenset(params.items())
        return role, frozenset()

    def make_unhashable(hashable_config):
        role, params_frozenset = hashable_config
        return {"role": role, "role_params": dict(params_frozenset)}

    hashable_configs = [make_hashable(c) for c in role_configs]
    all_perms_hashable = list(set(permutations(hashable_configs)))
    all_perms = [[make_unhashable(c) for c in p] for p in all_perms_hashable]
    return all_perms

