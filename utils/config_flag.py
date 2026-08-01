
def config_flag(name: str) -> Callable[[Match], Any]:
    """Function for extra_check to put pass behind a flag"""

    def flag_check(match: Match) -> Any:
        return getattr(config, name)

    return flag_check

