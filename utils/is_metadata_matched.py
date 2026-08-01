
def is_metadata_matched(config, entry_metadata):
    metadata_attrs = ["num_cpu_threads", "num_warps", "num_stages", "num_ctas"]
    for attr in metadata_attrs:
        if hasattr(config, attr) and hasattr(entry_metadata, attr):
            if getattr(config, attr) != getattr(entry_metadata, attr):
                return False
    return True

