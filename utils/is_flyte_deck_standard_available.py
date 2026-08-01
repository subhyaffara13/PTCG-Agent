
def is_flyte_deck_standard_available():
    if not is_flytekit_available():
        return False
    return importlib.util.find_spec("flytekitplugins.deck") is not None

