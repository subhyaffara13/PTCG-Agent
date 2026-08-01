
def _parse_option(
    cfg: configparser.RawConfigParser,
    cfg_opt_name: str,
    opt: str | None,
) -> list[str]:
    # specified on commandline: use that
    if opt is not None:
        return utils.parse_comma_separated_list(opt)
    else:
        # ideally this would reuse our config parsing framework but we need to
        # parse this from preliminary options before plugins are enabled
        for opt_name in (cfg_opt_name, cfg_opt_name.replace("_", "-")):
            val = cfg.get("flake8", opt_name, fallback=None)
            if val is not None:
                return utils.parse_comma_separated_list(val)
        else:
            return []

