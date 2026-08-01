
def _is_sharding_datapipe(datapipe: DataPipe) -> bool:
    return isinstance(datapipe, _ShardingIterDataPipe) or (
        hasattr(datapipe, "apply_sharding")
        and inspect.ismethod(datapipe.apply_sharding)
    )

