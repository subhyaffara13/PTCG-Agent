
def display_errors(errors: List['ErrorDict']) -> str:
    return '\n'.join(f'{_display_error_loc(e)}\n  {e["msg"]} ({_display_error_type_and_ctx(e)})' for e in errors)

