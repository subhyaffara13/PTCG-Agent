
def get_manager(
    device_index: int, create_if_none_exists: bool = True
) -> CUDAGraphTreeManager | None:
    if create_if_none_exists:
        return get_container(device_index).get_tree_manager()
    return get_container(device_index).tree_manager

