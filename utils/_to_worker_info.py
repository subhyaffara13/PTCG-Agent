
def _to_worker_info(to):
    if isinstance(to, WorkerInfo):
        return to
    elif isinstance(to, (str, int)):
        return get_worker_info(to)
    else:
        raise ValueError(f"Cannot get WorkerInfo from name {to}")

