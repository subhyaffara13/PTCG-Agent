
def _create_default_local_metadata(state_dict: STATE_DICT_TYPE) -> Metadata:
    """Return the ``Metadata`` if DefaultSavePlanner was used to checkpoint ``state_dict``."""
    plan = _create_default_metadata_only_plan(state_dict)
    _, md = create_default_global_save_plan([plan])
    return md

