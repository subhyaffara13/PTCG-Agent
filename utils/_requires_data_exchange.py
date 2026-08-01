
def _requires_data_exchange(padding, dim_map) -> bool:
    # Data exchange is not need if only sharded across batch dim
    if all(x == -1 for x in dim_map[1:]):
        return False
    # TODO: whether there requires data exchange is currently determined by padding
    return padding[-1] != 0

