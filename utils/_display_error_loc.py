
def _display_error_loc(error: 'ErrorDict') -> str:
    return ' -> '.join(str(e) for e in error['loc'])

