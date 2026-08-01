
def _traverse_helper(
    datapipe: DataPipe, only_datapipe: bool, cache: set[int]
) -> DataPipeGraph:
    if not isinstance(datapipe, (IterDataPipe, MapDataPipe)):
        raise RuntimeError(
            f"Expected `IterDataPipe` or `MapDataPipe`, but {type(datapipe)} is found"
        )

    dp_id = id(datapipe)
    if dp_id in cache:
        return {}
    cache.add(dp_id)
    # Using cache.copy() here is to prevent the same DataPipe pollutes the cache on different paths
    items = _list_connected_datapipes(datapipe, only_datapipe, cache.copy())
    d: DataPipeGraph = {dp_id: (datapipe, {})}
    for item in items:
        # Using cache.copy() here is to prevent recursion on a single path rather than global graph
        # Single DataPipe can present multiple times in different paths in graph
        # pyrefly: ignore [no-matching-overload]
        d[dp_id][1].update(_traverse_helper(item, only_datapipe, cache.copy()))
    return d

