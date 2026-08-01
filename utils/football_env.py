
def football_env():
    # Use lazy-import to avoid this heavy dependency unless it is really needed.
    return importlib.import_module("gfootball.env")

