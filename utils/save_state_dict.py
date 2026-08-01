
def save_state_dict(
    state_dict: STATE_DICT_TYPE,
    storage_writer: StorageWriter,
    process_group: dist.ProcessGroup | None = None,
    coordinator_rank: int = 0,
    no_dist: bool = False,
    planner: SavePlanner | None = None,
) -> Metadata:
    """This method is deprecated. Please switch to 'save'."""
    storage_writer.reset()

    # TODO: test returning `save` here instead.
    with _profile():
        return _save_state_dict(
            state_dict,
            storage_writer,
            process_group,
            coordinator_rank,
            no_dist,
            planner,
        )

