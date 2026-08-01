
def _write_generator_to_queue(queue: Queue[T], func: Callable[..., Iterable[T]], kwargs: dict) -> None:
    for result in func(**kwargs):
        queue.put(result)

