
def get_history_recording() -> AbstractContextManager[None]:
    # TODO - remove, prevents cleanup
    if not config.triton.cudagraph_trees_history_recording:
        return contextlib.nullcontext()
    return enable_history_recording()

