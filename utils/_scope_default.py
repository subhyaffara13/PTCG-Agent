
def _scope_default() -> defaultdict[str, list[_AccessNodes]]:
    # It's impossible to nest defaultdicts so we must use a function
    return defaultdict(list)

