
def reset_cudagraph_trees() -> None:
    "Clear all cudagraph trees"
    # see shutdown below for why this is necessary
    # Note: get_obj may fail if called from a thread that wasn't spawned by
    # autograd (e.g., test threads). In that case, there's nothing to reset.
    if not torch._C._is_key_in_tls("tree_manager_containers"):
        # TLS not set up for this thread, nothing to reset
        return
    container_dict = get_obj(local, "tree_manager_containers")
    locks_dict = get_obj(local, "tree_manager_locks")
    for device, lock in locks_dict.items():
        with lock:
            container = container_dict.get(device)
            if not container or not container.tree_manager:
                continue

            container.tree_manager.shutdown()

    _set_cached_tensors_enabled(False)
    container_dict.clear()

    MarkStepBox.mark_step_counter = 0

