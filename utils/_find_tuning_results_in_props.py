
def _find_tuning_results_in_props(metadata_props):
    for idx, prop in enumerate(metadata_props):
        if prop.key == _TUNING_RESULTS_KEY:
            return idx
    return -1

