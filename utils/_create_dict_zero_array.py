
def _create_dict_zero_array(space: Dict):
    return {key: create_zero_array(subspace) for key, subspace in space.spaces.items()}

