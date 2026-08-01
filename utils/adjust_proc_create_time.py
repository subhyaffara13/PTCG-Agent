
def adjust_proc_create_time(ctime):
    """Account for system clock updates."""
    if INIT_BOOT_TIME == 0:
        return ctime

    diff = INIT_BOOT_TIME - boot_time()
    if diff == 0 or abs(diff) < 1:
        return ctime

    debug("system clock was updated; adjusting process create_time()")
    if diff < 0:
        return ctime - diff
    return ctime + diff

