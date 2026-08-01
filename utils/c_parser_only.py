
def c_parser_only(request):
    """
    Fixture all of the CSV parsers using the C engine.
    """
    return request.param()

