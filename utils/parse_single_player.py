
def parse_single_player(obs_raw_entry):
    # Remove pixel information.
    if "frame" in obs_raw_entry:
        del obs_raw_entry["frame"]
    for k, v in obs_raw_entry.items():
        if type(v) == np.ndarray:
            obs_raw_entry[k] = v.tolist()
    return obs_raw_entry

