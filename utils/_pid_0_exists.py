
def _pid_0_exists():
    try:
        Process(0).name()
    except NoSuchProcess:
        return False
    except AccessDenied:
        return True
    else:
        return True

