
def win_service_get(name):
    """Open a Windows service and return it as a WindowsService instance."""
    service = WindowsService(name, None)
    service._display_name = service._query_config()['display_name']
    return service

