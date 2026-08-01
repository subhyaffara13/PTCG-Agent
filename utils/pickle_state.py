
def pickle_state(state):
    return _uarray._BackendState._unpickle, state._pickle()

