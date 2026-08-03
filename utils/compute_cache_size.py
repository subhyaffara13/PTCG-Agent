from typing import Any

def compute_cache_size(
    frame: DynamoFrameType, cache_entry: Any
) -> CacheSizeRelevantForFrame:
    # Walk the linked list to calculate the cache size
    num_cache_entries = 0
    num_cache_entries_with_same_id_matched_objs = 0

    while cache_entry:
        num_cache_entries += 1
        # Track the number of cache entries having same ID_MATCH'd objects as
        # that of frame.f_locals. This will be used later to compare against the
        # recompile_limit.
        if _has_same_id_matched_objs(frame, cache_entry):
            num_cache_entries_with_same_id_matched_objs += 1
        cache_entry = cache_entry.next

    return CacheSizeRelevantForFrame(
        num_cache_entries, num_cache_entries_with_same_id_matched_objs
    )

