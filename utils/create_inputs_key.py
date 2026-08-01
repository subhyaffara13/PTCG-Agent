
def create_inputs_key(input_nodes) -> str:
    return repr([AlgorithmSelectorCache.key_of(x) for x in input_nodes])

