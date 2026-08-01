
def parse_ini_file(f_loc):
    config = configparser.ConfigParser()
    try:
        config.read(f_loc)
        return {k: v for k, v in config.items("bandit")}

    except (configparser.Error, KeyError, TypeError):
        LOG.warning(
            "Unable to parse config file %s or missing [bandit] " "section",
            f_loc,
        )

    return None

