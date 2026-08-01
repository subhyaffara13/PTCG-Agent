
def _get_continue_on_failure(config: Config) -> bool:
    continue_on_failure: bool = config.getvalue("doctest_continue_on_failure")
    if continue_on_failure:
        # We need to turn off this if we use pdb since we should stop at
        # the first failure.
        if config.getvalue("usepdb"):
            continue_on_failure = False
    return continue_on_failure

