
def append_timestamp_to_dir(dir_path, append=True):
    if not append:
        return dir_path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = dir_path + f"_{timestamp}"
    return out

