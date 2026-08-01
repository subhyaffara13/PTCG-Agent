
def is_verbose(manager: BuildManager) -> bool:
    return manager.options.verbosity >= 1 or DEBUG_FINE_GRAINED

