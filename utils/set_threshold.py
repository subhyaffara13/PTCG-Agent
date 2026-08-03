import logging

def set_threshold(level: int) -> int:
    logging.root.setLevel(level * 10)
    return set_threshold.unpatched(level)


def set_threshold(level):
    orig = _global_log.level
    _global_log.setLevel(level)
    return orig

