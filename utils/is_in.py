
def is_in(item: T, *containers: Container[T]) -> bool:
    for container in containers:
        if item in container:
            return True
    return False

