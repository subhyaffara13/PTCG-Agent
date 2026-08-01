
def load_meltingpot(substrate_name: str):
    """Helper function to load Melting Pot substrates.

    Args:
        substrate_name: str

    Returns:
        env: meltingpot.utils.substrates.substrate.Substrate
    """
    import meltingpot
    from ml_collections import config_dict

    # Create env config
    substrate_name = substrate_name
    player_roles = meltingpot.substrate.get_config(substrate_name).default_player_roles
    env_config = {
        "substrate": substrate_name,
        "roles": player_roles,
    }

    # Build substrate from pickle
    env_config = config_dict.ConfigDict(env_config)
    env = meltingpot.substrate.build(env_config["substrate"], roles=env_config["roles"])
    return env

