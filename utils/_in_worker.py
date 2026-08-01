
def _in_worker():
    return bool(Worker._instances)

