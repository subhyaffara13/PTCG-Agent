
def _get_n(queue: "queue.Queue[JOB_ITEM_T]", n: int) -> list[JOB_ITEM_T]:
    return [queue.get() for _ in range(min(queue.qsize(), n))]

