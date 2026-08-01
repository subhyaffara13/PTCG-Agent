
def win_service_iter():
    """Yields a list of WindowsService instances."""
    for name, display_name in cext.winservice_enumerate():
        yield WindowsService(name, display_name)

