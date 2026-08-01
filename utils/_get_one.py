
def _get_one(queue: "queue.Queue[JOB_ITEM_T]") -> list[JOB_ITEM_T]:
    return [queue.get()]

