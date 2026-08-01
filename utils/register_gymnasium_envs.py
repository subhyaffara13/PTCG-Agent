
def register_gymnasium_envs():
    """This function is called when gymnasium is imported."""
    if "GymV26Environment-v0" in registry:
        registry.pop("GymV26Environment-v0")
    register(
        id="GymV26Environment-v0",
        entry_point="shimmy.openai_gym_compatibility:GymV26CompatibilityV0",
    )
    if "GymV21Environment-v0" in registry:
        registry.pop("GymV21Environment-v0")
    register(
        id="GymV21Environment-v0",
        entry_point="shimmy.openai_gym_compatibility:GymV21CompatibilityV0",
    )

    _register_bsuite_envs()
    _register_dm_control_envs()
    _register_dm_lab()

