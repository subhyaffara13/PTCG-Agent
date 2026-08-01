
def get_cudagraph_segments(pool_id: tuple[int, int]) -> Any:
    segments = torch.cuda.memory_snapshot()
    return [segment for segment in segments if segment["segment_pool_id"] == pool_id]

