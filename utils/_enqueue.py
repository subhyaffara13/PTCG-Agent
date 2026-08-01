
def _enqueue(queue: Queue, item: Node) -> None:  # type: ignore[type-arg]
    """
    Have a function to make it easier to do debug logging in a central place
    """
    queue.put(item)
    log.debug("Enqueue: %s", item)

