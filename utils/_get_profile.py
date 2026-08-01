
def _get_profile(config, profile_name, config_path):
    profile = {}
    if profile_name:
        profiles = config.get_option("profiles") or {}
        profile = profiles.get(profile_name)
        if profile is None:
            raise utils.ProfileNotFound(config_path, profile_name)
        LOG.debug("read in legacy profile '%s': %s", profile_name, profile)
    else:
        profile["include"] = set(config.get_option("tests") or [])
        profile["exclude"] = set(config.get_option("skips") or [])
    return profile

