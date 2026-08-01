
def parse_set_result(response, **options):
    """
    Handle SET result since GET argument is available since Redis 6.2.
    Parsing SET result into:
    - BOOL
    - String when GET argument is used
    """
    if options.get("get"):
        # Redis will return a getCommand result.
        # See `setGenericCommand` in t_string.c
        return response
    return response and str_if_bytes(response) == "OK"

